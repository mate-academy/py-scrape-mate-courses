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


def get_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    result = []
    for course in courses:
        name_elem = course.select_one(".typography_landingH3__vTjok")
        short_description_elem = course.select_one(
            ".CourseCard_courseDescription__Unsqj"
        )
        if "Вечірній" in name_elem.text:
            course_type = CourseType.PART_TIME
        else:
            course_type = CourseType.FULL_TIME
        result.append(Course(
            name=name_elem.text,
            short_description=short_description_elem.text,
            course_type=course_type))
    return result


courses = get_all_courses()

for course in courses:
    print(f"Name: {course.name}")
    print(f"Short Description: {course.short_description}")
    print(f"Course Type: {course.course_type.value}")
    print("----------------------------------------")
