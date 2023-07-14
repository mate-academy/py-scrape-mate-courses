from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def create_single_course(soup: Tag) -> Course:
    name = soup.select_one(".typography_landingH3__vTjok").text.split()

    return Course(
        name=name[1],
        short_description=soup.select_one(
            ".CourseCard_flexContainer__dJk4p"
        ).text,
        course_type=(
            CourseType.PART_TIME if len(name) == 3 else CourseType.FULL_TIME
        )
    )


def get_single_data(soup: BeautifulSoup) -> list[Course]:
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [create_single_course(page) for page in courses]


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    return get_single_data(soup)
