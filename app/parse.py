from typing import List
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    BOTH = ["full-time", "part-time"]


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    part_time_course = course_soup.find(
        "a",
        {"data-qa": "parttime-course-more-details-button"}
    )
    full_time_course = course_soup.find(
        "a",
        {"data-qa": "fulltime-course-more-details-button"}
    )

    if full_time_course and part_time_course:
        course_type = CourseType.BOTH
    elif full_time_course:
        course_type = CourseType.FULL_TIME
    elif part_time_course:
        course_type = CourseType.PART_TIME

    return Course(
        name=course_soup.find(
            "h3", class_="typography_landingH3__vTjok ProfessionCard_title__Zq5ZY mb-12"
        ).text,
        short_description=course_soup.find(
            "p", class_="typography_landingTextMain__Rc8BD mb-32"
        ).text,
        course_type=course_type
    )


def get_all_courses() -> List[Course]:
    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")

    courses = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [parse_single_course(course_soup) for course_soup in courses]


if __name__ == "__main__":
    get_all_courses()
