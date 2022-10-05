from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    count_of_modules: int
    count_of_topics: int
    duration: int


def get_additional_info(course_url: str) -> dict:
    course_info = requests.get(course_url).content
    soup = BeautifulSoup(course_info, "html.parser")
    info = soup.select_one(".CourseModulesHeading_headingGrid__50qAP")
    return {
        "count_of_modules": int(info.select_one(".CourseModulesHeading_text__EdrEk").text.split()[0]),
        "count_of_topics": int(info.select_one(".CourseModulesHeading_topicsNumber__PXMnR").text.split()[0]),
        "duration": info.select_one(".CourseModulesHeading_courseDuration__f_c3H").text.split()[0]
        if len(info) > 2 else None
    }


def get_single_course(course_soup: BeautifulSoup) -> Course:
    course_name = course_soup.select_one(".typography_landingH3__vTjok").text
    course_url = urljoin(BASE_URL, course_soup.select_one("a.mb-16")["href"])
    additional_info = get_additional_info(course_url)

    return Course(
        name=course_name,
        short_description=course_soup.select_one(".CourseCard_courseDescription__Unsqj").text,
        type=CourseType.PART_TIME
        if course_name.split()[-1] == "Вечірній"
        else CourseType.FULL_TIME,
        count_of_modules=additional_info["count_of_modules"],
        count_of_topics=additional_info["count_of_topics"],
        duration=additional_info["duration"]
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_single_course(course_soup) for course_soup in courses_soup]
