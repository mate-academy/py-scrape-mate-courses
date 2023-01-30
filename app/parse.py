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


def parse_single_course(
        course_type: CourseType,
        course_tag: Tag
) -> Course:
    return Course(
        name=course_tag.select_one(".typography_landingH3__vTjok").text,
        short_description=course_tag.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type
    )


def parse_course_type_with_courses(
        course_type: CourseType,
        courses_soup: BeautifulSoup
) -> list[Course]:
    courses = courses_soup.select(
        f"#{course_type.value} .CourseCard_cardContainer__7_4lK"
    )

    return [
        parse_single_course(
            course_type=course_type,
            course_tag=course
        )
        for course in courses
    ]


def get_all_courses() -> list[Course]:
    web_page = requests.get(BASE_URL).content
    soup = BeautifulSoup(web_page, "html.parser")
    courses = list()

    for course_type in CourseType:
        courses.extend(
            parse_course_type_with_courses(course_type, soup)
        )

    return courses


print(get_all_courses())
