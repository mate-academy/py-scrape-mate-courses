from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def parse_single_course(course_soup, course_type) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        type=course_type
    )


def get_courses(course_type):
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    course_format = soup.select_one(f"#{course_type.value}")
    courses = course_format.select(".CourseCard_cardContainer__7_4lK")

    return [
        parse_single_course(course_soup, course_type)
        for course_soup in courses
    ]


def get_all_courses() -> list[Course]:
    full = CourseType.FULL_TIME
    part = CourseType.PART_TIME
    return get_courses(full) + get_courses(part)
