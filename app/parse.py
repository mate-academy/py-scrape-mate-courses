from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup


LANDING_PAGE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup, course_type: CourseType
) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(LANDING_PAGE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")

    all_courses = []

    for course_type in CourseType:
        courses_soup = page_soup.select(
            f"#{course_type.value} .CourseCard_cardContainer__7_4lK"
        )

        all_courses.extend([
            parse_single_course(course_soup, course_type)
            for course_soup
            in courses_soup
        ])

    return all_courses
