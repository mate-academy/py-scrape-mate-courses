from dataclasses import dataclass
from enum import Enum
from typing import List

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
    course_type: CourseType


def parse_single_course(
        name: str,
        description: str,
        course_type: CourseType
) -> Course:
    return Course(
        name=name,
        short_description=description,
        course_type=course_type
    )


def parse_courses_from_html(soup: BeautifulSoup) -> List[Course]:
    course_soup = soup.select("section .CourseCard_cardContainer__7_4lK")
    courses = []

    for course in course_soup:
        name = course.select_one(".mb-16 span").text
        description = course.select_one(
            ".CourseCard_flexContainer__dJk4p p"
        ).text
        if len(name.split()) < 3:
            course_type = CourseType.FULL_TIME
        else:
            course_type = CourseType.PART_TIME

        courses.append(
            parse_single_course(name.split()[1], description, course_type)
        )

    return courses


def get_all_courses() -> List[Course]:
    req = requests.get(URL)
    soup = BeautifulSoup(req.content, "html.parser")
    courses = parse_courses_from_html(soup)
    return courses


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
