from typing import List
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: Tag) -> Course:
    type_of_course = course_soup.select_one("a.mb-16")["href"].split("-")[-1]

    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=(
            CourseType.PART_TIME
            if type_of_course == "parttime"
            else CourseType.FULL_TIME
        )
    )


def get_all_courses() -> List[Course]:
    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")

    courses = page_soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_single_course(course_soup) for course_soup in courses]
