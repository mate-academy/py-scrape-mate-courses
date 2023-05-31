from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

HOME_URL = "https://mate.academy/"

# CSS classes
NAME_CLASS = ".typography_landingH3__vTjok"
SHORT_DESCRIPTION_CLASS = ".CourseCard_courseDescription__Unsqj"
COURSE_CLASS = ".CourseCard_cardContainer__7_4lK"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(NAME_CLASS).text

    return Course(
        name=name,
        short_description=course_soup.select_one(
            SHORT_DESCRIPTION_CLASS
        ).text,
        course_type=CourseType(
            "part-time" if name.split(" ")[-1] == "Вечірній" else "full-time"
        )
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soap = BeautifulSoup(page, "html.parser")

    courses_soup = soap.select(COURSE_CLASS)

    return [get_single_course(course_soup) for course_soup in courses_soup]
