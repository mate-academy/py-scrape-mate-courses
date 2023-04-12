import requests

from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from enum import Enum


HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: Tag, course_type: CourseType) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=course_type
    )


def get_courses(course_type: CourseType) -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(
        f"#{course_type.value} .CourseCard_cardContainer__7_4lK"
    )
    return [
        parse_single_course(course_soup, course_type)
        for course_soup in courses
    ]


def get_all_courses() -> list[Course]:
    return [
        *get_courses(CourseType.FULL_TIME),
        *get_courses(CourseType.PART_TIME),
    ]
