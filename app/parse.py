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
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup,
        type_course: CourseType
) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=type_course,
    )


def parse_type_courses(
        type_soup: BeautifulSoup,
        type_course: CourseType
) -> [Course]:
    return [
        parse_single_course(course_soup, type_course)
        for course_soup in type_soup.select(".CourseCard_cardContainer__7_4lK")
    ]


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    return [
        *parse_type_courses(
            soup.select_one("#full-time > .large-6"),
            CourseType.FULL_TIME
        ),
        *parse_type_courses(soup.select_one(
            "#part-time > .large-6"),
            CourseType.PART_TIME
        ),
    ]


def main() -> None:
    print(get_all_courses())


if __name__ == "__main__":
    main()
