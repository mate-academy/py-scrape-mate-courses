from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup

import requests


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:

    return Course(
        name=course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get("https://mate.academy/").content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    parse_result = []

    for course_soup in courses:
        name = course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text
        if "Вечірній" in name:
            parse_result.append(
                parse_single_course(
                    course_soup, CourseType.PART_TIME
                ))
        else:
            parse_result.append(
                parse_single_course(
                    course_soup, CourseType.FULL_TIME
                ))

    return parse_result


if __name__ == "__main__":
    get_all_courses()
