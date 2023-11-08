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
    course_type: CourseType


def create_course(
    name: str, short_description: str, course_type: CourseType
) -> Course:
    return Course(name, short_description, course_type)


def get_all_courses() -> list[Course]:
    response = requests.get(URL).text
    soup = BeautifulSoup(response, "html.parser")
    cards_with_courses = soup.select("div.ProfessionCard_cardWrapper__JQBNJ")
    courses = []

    for course in cards_with_courses:
        name = course.select_one("h3.ProfessionCard_title__Zq5ZY").text
        short_description = course.select_one(".mb-32").text
        full_time = course.select_one(".Button_primary__7fH0C")
        part_time = course.select_one(".Button_secondary__DNIuD")

        if full_time:
            courses.append(
                create_course(name, short_description, CourseType.FULL_TIME)
            )

        if part_time:
            courses.append(
                create_course(name, short_description, CourseType.PART_TIME)
            )

    return courses
