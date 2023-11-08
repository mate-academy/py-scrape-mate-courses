from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: BeautifulSoup) -> list[Course]:
    name = course_soup.select_one("h3.typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text
    types = course_soup.select(".ButtonBody_buttonText__FMZEg")

    courses = []

    for course_type in types:
        if course_type.text == "Власний темп":
            courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.PART_TIME
                )
            )
        elif course_type.text == "Повний день":
            courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.FULL_TIME
                )
            )

    return courses


def get_all_courses() -> list:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_card = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []

    for course in courses_card:
        single_course = parse_single_course(course)
        all_courses.extend(single_course)

    return all_courses
