from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

HOME_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def parse_single_course(course_soup):
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".CourseCard_flexContainer__dJk4p"
    ).text
    course_type = (
        CourseType("part-time")
        if name.split()[-1] == "Вечірній"
        else CourseType("full-time")
    )

    return Course(
        name=name,
        short_description=short_description,
        type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


if __name__ == "__main__":
    get_all_courses()
