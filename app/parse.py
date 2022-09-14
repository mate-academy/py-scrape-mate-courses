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
    type: CourseType


def parse_single_course(course_soup) -> Course:
    print(dict(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one
        (".CourseCard_flexContainer__dJk4p > p"
         ).text,
        type="part-time" if "Вечірній" in str(
            course_soup.select_one(
                ".typography_landingH3__vTjok"
            ).text) else "full-time"
    ))


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_single_course(course_soup) for course_soup in courses]


get_all_courses()
