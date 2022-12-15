import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from enum import Enum

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: Tag) -> Course:
    name = course_soup.select_one(
        ".typography_landingH3__vTjok",
    ).text
    short_description = course_soup.select_one(
        ".typography_landingP1__N9PXd",
    ).text
    course_type = (
        (
            CourseType.PART_TIME
            if "Вечірній" in name
            else CourseType.FULL_TIME
        )
    )

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    coursers = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in coursers]
