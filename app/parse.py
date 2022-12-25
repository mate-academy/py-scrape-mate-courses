from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup

import requests


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:

    return Course(
        name=course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get("https://mate.academy/").content
    soup = BeautifulSoup(page, "html.parser")
    courses_full_time = soup.select(
        "#full-time > div > .CourseCard_cardContainer__7_4lK"
    )
    courses_part_time = soup.select(
        "#part-time > div > .CourseCard_cardContainer__7_4lK"
    )

    part_time = [
        parse_single_course(course_soup, CourseType.PART_TIME)
        for course_soup in courses_full_time
    ]
    full_time = [
        parse_single_course(course_soup, CourseType.FULL_TIME)
        for course_soup in courses_part_time
    ]

    return part_time + full_time


if __name__ == "__main__":
    get_all_courses()
