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
    duration: int


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:
    return Course(
        name=course_soup.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course_soup.select_one("p.mb-32").text,
        duration=int(
            course_soup.select_one(".ProfessionCard_subtitle__K1Yp6").text[:1]
        ),
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content

    soup = BeautifulSoup(page, "html.parser")

    courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    result = []
    for course in courses_soup:
        course_types_soup = course.select(".ButtonBody_buttonText__FMZEg")
        for single_ct_soup in course_types_soup:
            if single_ct_soup.text == "Власний темп":
                course_type = CourseType.PART_TIME
            else:
                course_type = CourseType.FULL_TIME
            result.append(parse_single_course(course, course_type))
    return result
