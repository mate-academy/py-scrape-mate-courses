from dataclasses import dataclass
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


BASE_URL = "https://mate.academy/"


def make_request() -> bytes:
    response = requests.get(BASE_URL)
    return response.content


def scrape_all_courses(response: bytes) -> List[str]:
    soup = BeautifulSoup(response, features="html.parser")
    return soup.find_all(
        "div",
        class_="ProfessionCard_cardWrapper__JQBNJ"
    )


def map_course_type(course_type: str) -> CourseType:
    if course_type == "Повний день":
        return CourseType.FULL_TIME

    return CourseType.PART_TIME


def scrape_single_course(course: str) -> List[Course]:
    course_name = course.find("h3").text
    course_short_description = course.find(
        "p",
        class_="typography_landingTextMain__Rc8BD mb-32"
    ).text

    course_types = []
    for course_type in course.find(
            "div",
            class_="ProfessionCard_buttons__a0o60"
    ).find_all("a"):
        course_types.append(map_course_type(course_type.text))

    courses_list = []
    for course_type in course_types:
        courses_list.append(
            Course(
                name=course_name,
                short_description=course_short_description,
                course_type=course_type
            )
        )

    return courses_list


def get_all_courses() -> List[Course]:
    response = make_request()
    all_courses = scrape_all_courses(response)
    courses = []
    for course in all_courses:
        courses.extend(scrape_single_course(course))
    return courses


if __name__ == "__main__":
    print(get_all_courses())
