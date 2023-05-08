from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

MAIN_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    href: str
    short_description: str
    course_type: CourseType


def make_course_object(
        course: BeautifulSoup, course_type: CourseType
) -> Course:
    name = course.find("a").text.replace("Курс ", "")
    href = MAIN_URL + course.find("a").get("href")
    description = course.find(
        "p", {"class": "CourseCard_courseDescription__Unsqj"}
    ).text

    return Course(
        name=name,
        href=href,
        short_description=description,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    response = requests.get(MAIN_URL).content
    soup = BeautifulSoup(response, "html.parser")

    courses_html = {
        "full-time": soup.find_all(
            "section", {"class": "CourseCard_cardContainer__7_4lK"}
        ),
        "part-time": soup.find_all(
            "section", {"class": "CourseCard_cardContainer__7_4lK"}
        ),
    }

    full_time_list = [
        make_course_object(course=course, course_type=CourseType.FULL_TIME)
        for course
        in courses_html.get("full-time")
    ]
    part_time_list = [
        make_course_object(course=course, course_type=CourseType.PART_TIME)
        for course
        in courses_html.get("part-time")
    ]

    return full_time_list + part_time_list


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
