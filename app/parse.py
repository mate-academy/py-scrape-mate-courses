from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def create_course(course_soup: Tag, full_time: bool = False) -> Course:
    if full_time:
        course_type = CourseType.FULL_TIME
    else:
        course_type = CourseType.PART_TIME

    return Course(
        name=course_soup.select_one("h3").text,
        short_description=course_soup.select_one(".mb-32").text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    soup_courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []

    for course in soup_courses:
        all_courses.append(create_course(course))

        if course.select_one("a[data-qa^='full']"):
            all_courses.append(create_course(course, full_time=True))

    return all_courses
