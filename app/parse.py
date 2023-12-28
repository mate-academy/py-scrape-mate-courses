from dataclasses import dataclass, fields
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


QUOTE_FIELDS = [field.name for field in fields(Course)]


def get_course_type(course_soup: BeautifulSoup) -> [CourseType]:
    full_time = course_soup.select_one(".Button_secondary__DNIuD")
    part_time = course_soup.select_one(
        ".Button_primary__7fH0C.Button_large__rIMVg"
    )
    course_type = []
    if full_time is not None:
        course_type.append(CourseType.FULL_TIME)
    if part_time is not None:
        course_type.append(CourseType.PART_TIME)
    return course_type


def parse_single_course(course_soup: BeautifulSoup) -> [Course]:
    courses = []
    name = course_soup.select_one(
        ".typography_landingH3__vTjok.ProfessionCard_title__Zq5ZY"
    ).text
    short_description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text

    course_type = get_course_type(course_soup)

    if CourseType.PART_TIME in course_type:
        courses.append(Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.PART_TIME
        ))

    if CourseType.FULL_TIME in course_type:
        courses.append(Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.FULL_TIME
        ))

    return courses


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    unparsed_courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    courses_lists = [
        parse_single_course(course_soup) for course_soup in unparsed_courses
    ]
    courses = [element for sublist in courses_lists for element in sublist]

    return courses


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
