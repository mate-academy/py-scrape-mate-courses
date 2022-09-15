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


def parse_single_course(course_soup) -> Course:
    course_title = course_soup.select_one(".typography_landingH3__vTjok").text
    single_course = dict(
        name=course_title,
        short_description=course_soup.select_one
        (".CourseCard_flexContainer__dJk4p > p"
         ).text,
        type=CourseType("part-time") if "Вечірній" in course_title
        else CourseType("full-time")
    )

    return Course(
        name=single_course["name"],
        short_description=single_course["short_description"],
        type=single_course["type"]
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_single_course(course_soup) for course_soup in courses]


get_all_courses()
