from typing import List
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


def parse_single_course(course_card: BeautifulSoup) -> List[CourseType]:
    course_types = course_card.select(
        ".ProfessionCard_buttons__a0o60 > a[data-qa]"
    )
    return [
        CourseType.FULL_TIME if "fulltime" in course_type["data-qa"]
        else CourseType.PART_TIME
        for course_type in course_types
    ]


def get_all_courses() -> List[Course]:
    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")
    courses_card_soup = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []
    for course_card in courses_card_soup:
        name = course_card.find("h3", class_="mb-12").text
        short_description = course_card.find("p", class_="mb-32").text
        course_types = parse_single_course(course_card)

        for course_type in course_types:
            course = Course(
                name=name,
                short_description=short_description,
                course_type=course_type)
            all_courses.append(course)

    return all_courses
