from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup, Tag


HOME_URL = "https://mate.academy/en/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_course(course_soup: Tag, course_type: CourseType) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=course_type,
    )


def get_full_time_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")
    full_time_courses = soup.select(
        "#full-time .CourseCard_cardContainer__7_4lK"
    )
    return [
        parse_course(course_soup, "full_time")
        for course_soup in full_time_courses
    ]


def get_part_time_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")
    part_time_courses = soup.select(
        "#part-time .CourseCard_cardContainer__7_4lK"
    )
    return [
        parse_course(course_soup, "part_time")
        for course_soup in part_time_courses
    ]


def get_all_courses() -> list[Course]:
    return [get_full_time_courses(), get_part_time_courses()]


if __name__ == '__main__':
    print(get_all_courses())
