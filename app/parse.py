import requests

from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from enum import Enum


BASE_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_card: Tag) -> list[Course]:
    courses = []

    name = course_card.select_one(".mb-12").text
    short_description = course_card.select_one(".mb-32").text

    course_types_soup = course_card.select("a[data-qa]")
    for course_type in course_types_soup:
        if "fulltime" in course_type["data-qa"]:
            course_type = CourseType.FULL_TIME
        elif "parttime" in course_type["data-qa"]:
            course_type = CourseType.PART_TIME

        course = Course(
            name=name,
            short_description=short_description,
            course_type=course_type
        )
        courses.append(course)

    return courses


def get_all_courses() -> list[Course]:
    courses_list = []

    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    course_cards = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    for course_card in course_cards:

        courses_list.extend(parse_single_course(course_card))

    return courses_list
