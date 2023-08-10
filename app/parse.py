from dataclasses import dataclass, fields
from enum import Enum
from bs4 import BeautifulSoup, Tag
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


QUOTE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course_container: Tag) -> Course:
    name = course_container.select_one(
        "a span.typography_landingH3__vTjok"
    ).text.strip()

    short_description = course_container.select_one(
        "p.typography_landingMainText__Ux18x"
    ).text.strip()

    course_type = (
        CourseType.PART_TIME
        if "flex" in name
        else CourseType.FULL_TIME
    )

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    course_elements = soup.select(".CourseCard_cardContainer__7_4lK")

    return [
        parse_single_course(course_element)
        for course_element in course_elements
    ]
