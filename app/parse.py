from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_of_modules: int
    num_of_topics: int
    num_of_duration: str


def get_detail_page(course_soup: Tag) -> BeautifulSoup:
    detail_url = course_soup.select_one("a")["href"][1:]
    page = requests.get(BASE_URL + detail_url).content
    soup = BeautifulSoup(page, "html.parser")

    return soup


def get_one_course(course_soup: Tag) -> Course:
    name_of_course = course_soup.select_one(
        ".typography_landingH3__vTjok"
    ).text
    description_of_course = course_soup.select_one(
        ".typography_landingP1__N9PXd"
    ).text
    course_type = (
        CourseType.PART_TIME
        if "Вечірній" in name_of_course
        else CourseType.FULL_TIME
    )

    detail_page = get_detail_page(course_soup)
    num_of_modules = detail_page.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text
    num_of_topics = detail_page.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text
    num_of_duration = (
        str(
            detail_page.select_one(
                ".CourseModulesHeading_courseDuration__f_c3H"
            ).text
        )
        if course_type == CourseType.FULL_TIME
        else "Навчайся у власному графіку"
    )

    return Course(
        name=name_of_course,
        short_description=description_of_course,
        course_type=course_type,
        num_of_modules=int(num_of_modules.split()[0]),
        num_of_topics=int(num_of_topics.split()[0]),
        num_of_duration=num_of_duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_one_course(course) for course in courses]
