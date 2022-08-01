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
    type: CourseType


def get_all_courses() -> list[Course]:
    list_of_courses = []

    target_page = requests.get(BASE_URL).content
    soup = BeautifulSoup(target_page, "html.parser")
    courses = soup.select(
        ".section_scrollSection__RBDyT .CourseCard_cardContainer__7_4lK"
    )

    for course in courses:

        name_of_course = course.select_one(
            ".typography_landingH3__vTjok"
        ).text
        short_description = course.select_one(
            ".typography_landingP1__N9PXd"
        ).text
        course_type = CourseType.FULL_TIME

        if name_of_course.split()[-1] == "Вечірній":
            course_type = CourseType.PART_TIME

        the_course = Course(
            name=name_of_course,
            short_description=short_description,
            type=course_type
        )

        list_of_courses.append(the_course)

    return list_of_courses


def main():
    return get_all_courses()


if __name__ == "__main__":
    main()
