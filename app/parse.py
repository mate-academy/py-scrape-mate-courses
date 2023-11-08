from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def check_course_type(course_card: BeautifulSoup) -> list[CourseType]:
    course_types = course_card.select(
        ".ProfessionCard_buttons__a0o60 > a[data-qa]"
    )
    return [
        CourseType.FULL_TIME if "fulltime" in course_type["data-qa"]
        else CourseType.PART_TIME
        for course_type in course_types
    ]


def get_course_by_spec(course_card: BeautifulSoup) -> list[Course]:
    return [
        Course(
            name=course_card.select_one(".mb-12").text,
            short_description=course_card.select_one(".mb-32").text,
            course_type=course_type
        )
        for course_type in check_course_type(course_card)
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    course_cards = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []
    for course_card in course_cards:
        all_courses.extend(get_course_by_spec(course_card))

    return all_courses
