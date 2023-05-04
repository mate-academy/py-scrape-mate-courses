from dataclasses import dataclass
from enum import Enum

import requests

from bs4 import BeautifulSoup

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    modules: int
    topics: int
    course_type: CourseType


def parse_single_course(soup: BeautifulSoup, course_type: str) -> Course:
    detail_page_url = (
        URL + soup.select_one("a.CourseCard_button__HTQvE")["href"]
    )
    detail_page = requests.get(detail_page_url)
    detail_page.raise_for_status()
    detail_soup = BeautifulSoup(detail_page.content.decode(), "html.parser")

    modules_number = int(
        detail_soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP > p"
        ).text.split()[0]
    )
    topics_number = int(
        detail_soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR > p"
        ).text.split()[0]
    )

    if course_type == CourseType.FULL_TIME.value:
        name = " ".join(
            soup.select_one(".typography_landingH3__vTjok").text.split()[1:]
        )
    elif course_type == CourseType.PART_TIME.value:
        name = " ".join(
            soup.select_one(".typography_landingH3__vTjok").text.split()[1:-1]
        )

    short_description = soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course = Course(
        name=name,
        short_description=short_description,
        modules=modules_number,
        topics=topics_number,
        course_type=CourseType(course_type),
    )

    return course


def get_all_courses() -> list[Course]:
    page = requests.get(URL)
    page.raise_for_status()
    soup = BeautifulSoup(page.content.decode(), "html.parser")

    full_time_courses = soup.select(
        "#full-time .CourseCard_cardContainer__7_4lK"
    )
    part_time_courses = soup.select(
        "#part-time .CourseCard_cardContainer__7_4lK"
    )

    courses = [
        parse_single_course(course, CourseType.FULL_TIME.value)
        for course in full_time_courses
    ]
    courses.extend(
        [
            parse_single_course(course, CourseType.PART_TIME.value)
            for course in part_time_courses
        ]
    )

    return courses


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(
            f"{course.name} ({course.course_type}): "
            f"{course.short_description} - Modules: {course.modules},"
            f" Topics: {course.topics}"
        )
