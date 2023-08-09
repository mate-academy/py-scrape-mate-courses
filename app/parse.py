from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

SITE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def convert_to_course_instance(course_soup: Tag, course_type: str) -> Course:
    return Course(
        name=course_soup.select_one("a").text,
        short_description=course_soup.select_one("div > p").text,
        course_type=CourseType(course_type)
    )


def get_courses(soup: BeautifulSoup, course_type: str) -> list:
    return [convert_to_course_instance(
        course_soup=course,
        course_type=course_type
    ) for course in soup.select(
        f"div#{course_type} > div.large-offset-1 > section"
    )]


def get_all_courses() -> list[Course]:
    page = requests.get(SITE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    return get_courses(soup, "part-time") + get_courses(soup, "full-time")
