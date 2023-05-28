from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/ru/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: Tag) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text.strip()
    return Course(
        name=name,
        short_description=course_soup.select_one("p").text,
        course_type=(
            CourseType.PART_TIME
            if "Вечерний" in name else
            CourseType.FULL_TIME
        ),
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    full_time_soup = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in full_time_soup]
