from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

MATE_HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course_card(course_soup: Tag) -> list[Course]:
    name = course_soup.select_one(
        "a.ProfessionCard_title__Zq5ZY"
    ).text
    short_description = course_soup.select_one(
        "p.typography_landingTextMain__Rc8BD"
    ).text
    course_type = CourseType.PART_TIME

    course = Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )
    print(f"parsing {name}, part-time")

    if not course_soup.select_one(
            "a[data-qa='fulltime-course-more-details-button']"
    ):
        return [course]

    print(f"parsing {name}, full-time")
    course_full_time = Course(
        name=name,
        short_description=short_description,
        course_type=(
            CourseType.FULL_TIME
        )
    )

    return [course, course_full_time]


def get_all_courses() -> list[Course]:
    content = requests.get(MATE_HOME_URL).content
    soup = BeautifulSoup(
        content, "html.parser"
    ).select(".ProfessionCard_cardWrapper__JQBNJ")
    courses = []
    for course_card in soup:
        courses.extend(parse_single_course_card(course_card))
    return courses
