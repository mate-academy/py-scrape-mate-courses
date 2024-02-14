from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(course: Tag) -> [Course]:
    course_name = course.select_one("a").text
    course_description = course.select_one(".mb-32").text
    all_course_types = course.select(".ButtonBody_buttonText__FMZEg")

    course_types = {
        "Повний день": CourseType.FULL_TIME,
        "Власний темп": CourseType.PART_TIME,
    }

    return [
        Course(
            name=course_name,
            short_description=course_description,
            course_type=course_types[course.text],
        ) for course in all_course_types
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_mate_courses = []

    for course in courses_soup:
        all_mate_courses.extend(get_single_course(course))

    return all_mate_courses


if __name__ == "__main__":
    get_all_courses()
