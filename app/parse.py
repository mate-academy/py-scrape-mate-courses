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


def parse_single_course(course_soup: BeautifulSoup, course_type: str) -> Course:
    return Course(
        name=course_soup.select_one("section > a > span").text.split()[1],
        short_description=course_soup.select_one("section > div > p").text,
        course_type=CourseType(course_type),
    )


def get_courses_by_course_type(page_soup: BeautifulSoup, course_type: str) -> list[Course]:
    return [
        parse_single_course(course_soup=course, course_type=course_type)
        for course in page_soup.select_one(f"div#{course_type} > .large-offset-1")
    ]


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")

    return get_courses_by_course_type(soup, "part-time") + get_courses_by_course_type(soup, "full-time")


if __name__ == "__main__":
    get_all_courses()
