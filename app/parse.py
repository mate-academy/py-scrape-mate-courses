from dataclasses import dataclass
from enum import Enum
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    count_of_modules: int
    count_of_topics: int
    course_duration: int


def get_modules_topics_duration(course_link: str) -> tuple[int, int, int]:
    url = urljoin(BASE_URL, course_link)
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")

    count_of_modules = int(soup.find(
        "div",
        {"class": "CourseModulesHeading_modulesNumber__GNdFP"}
    ).text.split()[0])
    count_of_topics = int(soup.find(
        "div",
        {"class": "CourseModulesHeading_topicsNumber__PXMnR"}
    ).text.split()[0])
    course_duration = int(soup.find(
        "div",
        {"class": "CourseModulesHeading_courseDuration__f_c3H"}
    ).text.split()[0])

    return count_of_modules, count_of_topics, course_duration


def check_full_time(
        course_soup: BeautifulSoup,
        name: str,
        short_description: str
) -> Course | None:
    block = course_soup.find(
        "a",
        {"data-qa": "fulltime-course-more-details-button"}
    )
    if block:
        course_link = block.get("href")
        (
            count_of_modules,
            count_of_topics,
            course_duration
        ) = get_modules_topics_duration(course_link)
        full_time = Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.FULL_TIME,
            count_of_modules=count_of_modules,
            count_of_topics=count_of_topics,
            course_duration=course_duration
        )
        return full_time


def check_part_time(
        course_soup: BeautifulSoup,
        name: str,
        short_description: str
) -> Course | None:
    block = course_soup.find(
        "a",
        {"data-qa": "parttime-course-more-details-button"}
    )
    if block:
        course_link = block.get("href")
        (
            count_of_modules,
            count_of_topics,
            course_duration
        ) = get_modules_topics_duration(course_link)
        part_time = Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.PART_TIME,
            count_of_modules=count_of_modules,
            count_of_topics=count_of_topics,
            course_duration=course_duration
        )
        return part_time


def parse_single_course(
        course_soup: BeautifulSoup
) -> tuple[Optional[Course], Optional[Course]]:
    name = course_soup.select_one(
        ".typography_landingH3__vTjok.ProfessionCard_title__fTqBr.mb-12"
    ).text
    short_description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text

    part_time = check_part_time(
        course_soup=course_soup,
        name=name,
        short_description=short_description
    )
    full_time = check_full_time(
        course_soup=course_soup,
        name=name,
        short_description=short_description
    )
    return part_time, full_time


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__DnW_d")

    return [
        each_course
        for course_type in courses
        for each_course in parse_single_course(course_type) if each_course
    ]


if __name__ == "__main__":
    result = get_all_courses()
    for i in result:
        print(i)
