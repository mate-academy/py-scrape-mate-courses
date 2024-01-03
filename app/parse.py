from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

MATE_LANDING_PAGE = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def create_course_instance(course_soup: BeautifulSoup) -> Course:
    name = course_soup.text.replace(" flex", "")
    course_type = (CourseType.PART_TIME
                   if "flex" in course_soup.text else CourseType.FULL_TIME)
    short_description = f"Course name: {name}, Type: {course_type.value}"

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_courses_soup() -> BeautifulSoup:
    page = requests.get(MATE_LANDING_PAGE).content
    page_soup = BeautifulSoup(page, "html.parser")

    return page_soup.select("div.cell.large-8 > ul > li > div > a > span")


def get_all_courses() -> list[Course]:
    return [
        create_course_instance(course_soup)
        for course_soup in get_courses_soup()
    ]


def main() -> None:
    courses = get_all_courses()
    for course in courses:
        print(course)


main()
