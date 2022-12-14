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


def create_single_course(course_soup, time):
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(".CourseCard_flexContainer__dJk4p").text,
        course_type=CourseType.FULL_TIME if CourseType.FULL_TIME.value == time else CourseType.PART_TIME
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select_one("#all-courses").select(".section_scrollSection__RBDyT")
    coursers_list = []

    for course_group in courses:
        time = course_group["id"]

        for course in course_group.select(".CourseCard_cardContainer__7_4lK"):
            coursers_list.append(create_single_course(course, time))

    return coursers_list


if __name__ == "__main__":
    get_all_courses()
