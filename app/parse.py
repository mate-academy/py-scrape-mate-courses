import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum

MATE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_course_type(page_soup: BeautifulSoup) -> list[CourseType]:
    courses_type = page_soup.select(
        ".ProfessionCard_buttons__a0o60 a[data-qa]"
    )

    return [
        CourseType.PART_TIME if "parttime" in course_type["data-qa"]
        else CourseType.FULL_TIME for course_type in courses_type
    ]


def get_single_course(page_soup: BeautifulSoup) -> list[Course]:
    name = page_soup.select_one(
        ".typography_landingH3__vTjok"

    ).text
    short_description = page_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text

    return [
        Course(
            name=name,
            short_description=short_description,
            course_type=course_type
        ) for course_type in get_course_type(page_soup)
    ]


def get_all_courses() -> list[Course]:

    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    course_cards = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []
    for course_card in course_cards:
        all_courses.extend(get_single_course(course_card))

    return all_courses
