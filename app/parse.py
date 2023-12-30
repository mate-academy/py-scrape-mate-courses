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


def parse_course(course_soup: BeautifulSoup) -> [Course]:
    courses = []
    course_name = course_soup.select_one("h3").text
    course_short_description = course_soup.select(
        ".typography_landingTextMain__Rc8BD"
    )[1].text
    course_full_time = course_soup.select_one(".Button_primary__7fH0C")
    course_part_time = course_soup.select_one(".Button_secondary__DNIuD")

    if course_full_time:
        courses.append(
            Course(
                name=course_name,
                short_description=course_short_description,
                course_type=CourseType.FULL_TIME
            )
        )
    if course_part_time:
        courses.append(
            Course(
                name=course_name,
                short_description=course_short_description,
                course_type=CourseType.PART_TIME
            )
        )

    return courses


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []

    for course_soup in courses_soup:
        all_courses.extend(parse_course(course_soup))

    return all_courses
