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
    type: CourseType


def get_single_course(course_soup: BeautifulSoup) -> Course:

    course_name = course_soup.select_one(".typography_landingH3__vTjok").text
    return Course(
        name=course_name,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        type=CourseType.PART_TIME
        if course_name.split()[-1] == "Вечірній"
        else CourseType.FULL_TIME,
    )


def get_all_courses() -> list[Course]:

    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_soup = soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_single_course(course_soup=course_soup)
            for course_soup in courses_soup]
