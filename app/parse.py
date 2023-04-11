from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

MATE_ACADEMY_HOME_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_type(course_soup: BeautifulSoup) -> CourseType:
    course_type = course_soup.find_parent(
        class_="section_scrollSection__RBDyT"
    ).get("id")
    return CourseType(course_type)


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one(
            ".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd").text,
        course_type=get_single_type(course_soup)
    )


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_ACADEMY_HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    all_courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in all_courses]


if __name__ == "__main__":
    print(get_all_courses())
