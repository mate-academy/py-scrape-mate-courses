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
    course_type: CourseType


def parse_course(course_soup: BeautifulSoup) -> Course:
    course_name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = (
        CourseType.PART_TIME if "Вечірній" in course_name
        else CourseType.FULL_TIME
    )
    return Course(course_name, short_description, course_type)


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_course(course) for course in courses]
