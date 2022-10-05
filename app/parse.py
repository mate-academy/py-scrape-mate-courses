from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def parse_single_course(course_soup: BeautifulSoup) -> [Course]:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        type=CourseType.PART_TIME
        if course_soup.select_one(".typography_landingH3__vTjok").text.split()[-1] == "Вечірній"
        else CourseType.FULL_TIME
    )


# def get_single_page


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    all_courses = [parse_single_course(course) for course in courses]

    return all_courses


get_all_courses()
