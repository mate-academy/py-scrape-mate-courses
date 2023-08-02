from dataclasses import dataclass
from enum import Enum

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


def get_single_course(course_soup: BeautifulSoup, course_type: str) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".typography_landingMainText__Ux18x"
        ).text,
        course_type=CourseType(course_type)
    )


def get_courses_type(
        page_soup: BeautifulSoup,
        course_type: str
) -> list[Course]:
    courses = page_soup.select(
        f"#{course_type} .CourseCard_cardContainer__7_4lK"
    )
    return [get_single_course(course, course_type) for course in courses]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    all_courses = (
        get_courses_type(
            soup, "full-time"
        ) + get_courses_type(soup, "part-time")
    )

    return all_courses
