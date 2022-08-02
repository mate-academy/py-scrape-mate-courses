from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def check_course_type(soup: BeautifulSoup) -> str:
    course_type = soup.select_one("a").text.split()[-1]
    if course_type == "Вечірній":
        return "part-time"

    return "full-time"


def parse_single_course(soup: BeautifulSoup) -> Course:
    course_type = check_course_type(soup)
    return Course(
        name=soup.select_one("a").text,
        short_description=soup.select_one("div > p").text,
        type=CourseType(course_type)
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(
        ".large-offset-1 > .CourseCard_cardContainer__7_4lK"
    )

    parsed_courses = [
        parse_single_course(course_soup) for course_soup in courses
    ]

    return parsed_courses
