from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

HOME_URL = "https://mate.academy/"

# CSS classes
name_class = ".typography_landingH3__vTjok"
short_description_class = ".CourseCard_courseDescription__Unsqj"
course_class = ".CourseCard_cardContainer__7_4lK"


class CourseType(Enum):
    FULL_TIME = False
    PART_TIME = True


# class CourseType(Enum):
#     FULL_TIME = "full-time"
#     PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(name_class).text

    return Course(
        name=name,
        short_description=course_soup.select_one(
            short_description_class
        ).text,
        course_type=CourseType(name[-1] == "й")
        # course_type=CourseType(
        #     "part-time" if name[-1] == "й" else "full-time"
        # )
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soap = BeautifulSoup(page, "html.parser")

    courses_soup = soap.select(course_class)

    return [get_single_course(course_soup) for course_soup in courses_soup]
