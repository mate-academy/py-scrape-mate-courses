from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

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
    num_modules: int
    num_topics: int
    months: int
    course_type: CourseType


def get_course_program(
        course_soup: BeautifulSoup, course_type: CourseType
) -> tuple[int]:
    link_to_program = course_soup.select_one("a")["href"]
    page = requests.get(urljoin(BASE_URL, link_to_program)).content
    soup = BeautifulSoup(page, "html.parser")

    modules = int(
        soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP > p"
        ).text.split()[0]
    )
    topics = int(
        soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR > p"
        ).text.split()[0]
    )
    if course_type == CourseType.FULL_TIME:
        duration = int(
            soup.select_one(
                ".CourseModulesHeading_courseDuration__f_c3H > p"
            ).text.split()[0]
        )
    else:
        duration = None

    return modules, topics, duration


def parse_single_course(
    course_soup: BeautifulSoup, course_type: CourseType
) -> Course:
    modules, topics, duration = get_course_program(course_soup, course_type)

    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        num_modules=modules,
        num_topics=topics,
        months=duration,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_courses_soup = soup.select(
        "#full-time .CourseCard_cardContainer__7_4lK"
    )
    part_time_courses_soup = soup.select(
        "#part-time .CourseCard_cardContainer__7_4lK"
    )

    full_time = [
        parse_single_course(course_soup, CourseType.FULL_TIME)
        for course_soup in full_time_courses_soup
    ]
    part_time = [
        parse_single_course(course_soup, CourseType.PART_TIME)
        for course_soup in part_time_courses_soup
    ]

    full_time.extend(part_time)
    return full_time


if __name__ == "__main__":
    get_all_courses()
