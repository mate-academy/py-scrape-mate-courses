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


def parse_single_course(soup: BeautifulSoup, course_type: str) -> Course:
    return Course(
        name=soup.select_one("a").text,
        short_description=soup.select_one("div > p").text,
        type=CourseType(course_type)
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_courses = soup.select(
        "div#full-time > div.large-offset-1 > .CourseCard_cardContainer__7_4lK"
    )
    part_time_courses = soup.select(
        "div#part-time > div.large-offset-1 > .CourseCard_cardContainer__7_4lK"
    )

    parsed_full_time = [
        parse_single_course(soup, "full-time") for soup in full_time_courses
    ]
    parsed_part_time = [
        parse_single_course(soup, "part-time") for soup in part_time_courses
    ]

    return parsed_full_time + parsed_part_time
