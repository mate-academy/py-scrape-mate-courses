import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum


BASE_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(course: BeautifulSoup) -> Course:
    course_type_in_url = course.select_one("a.mb-16")["href"].split("-")[-1]
    course_details = dict(
        name=course.select_one(".typography_landingH3__vTjok").text,
        short_description=course.select_one(
            "p.CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=(
            CourseType.PART_TIME
            if course_type_in_url == "parttime"
            else CourseType.FULL_TIME
        )
    )

    return Course(
        **course_details
    )


def get_all_courses() -> list[Course]:
    page_content = requests.get(BASE_URL).content
    base_soup = BeautifulSoup(page_content, "html.parser")

    courses = base_soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_single_course(course) for course in courses]
