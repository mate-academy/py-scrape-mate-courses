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


def get_unit_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one("h3").text
    description = course_soup.select_one(".mb-32").text
    course_types = [
        course_type.text
        for course_type in
        course_soup.select(".ButtonBody_buttonText__FMZEg")
    ]
    choices = {
        "Власний темп": CourseType.PART_TIME,
        "Повний день": CourseType.FULL_TIME
    }
    return [
        Course(
            name=name,
            short_description=description,
            course_type=choices[course_type]
        ) for course_type in course_types
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select("div.ProfessionCard_cardWrapper__JQBNJ")

    return [
        course
        for unit_course in courses
        for course in get_unit_course(unit_course)
    ]


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
