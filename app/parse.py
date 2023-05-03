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


def parse_single_full_time_course(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(".CourseCard_courseDescription__Unsqj").text,
        course_type=CourseType.FULL_TIME,
    )


def parse_single_part_time_course(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(".CourseCard_courseDescription__Unsqj").text,
        course_type=CourseType.PART_TIME,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    courses_list_full_time = [parse_single_full_time_course(course_soup) for course_soup in courses]
    courses_list_part_time = [parse_single_part_time_course(course_soup) for course_soup in courses]
    return courses_list_full_time + courses_list_part_time
