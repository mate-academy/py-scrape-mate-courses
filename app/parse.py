from dataclasses import dataclass
from enum import Enum

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    modules_count: int
    topics_count: int
    duration: int
    course_type: CourseType


def check_course_type(course_name: str) -> CourseType:
    if "Вечірній" in course_name:
        return CourseType.PART_TIME
    return CourseType.FULL_TIME


def get_course_counting(course_url: str) -> tuple[int, int, int | None]:
    page = requests.get(course_url).content
    soup = BeautifulSoup(page, "html.parser")

    modules_count = int(
        soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP > p"
        ).text.split()[0]
    )
    topics_count = int(
        soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR > p"
        ).text.split()[0]
    )

    duration = soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H > p"
    )

    if duration:
        duration_count = duration.text.split()[0]
    else:
        duration_count = None

    return modules_count, topics_count, duration_count


def get_one_course(course_soup: BeautifulSoup | Tag) -> Course:
    course_url = urljoin(URL, course_soup.select_one("a")["href"])

    modules_count, topics_count, duration = get_course_counting(course_url)
    course_name = course_soup.select_one(
        "span.typography_landingH3__vTjok"
    ).text
    short_description = course_soup.select_one(
        "p.CourseCard_courseDescription__Unsqj"
    ).text

    return Course(
        name=course_name,
        short_description=short_description,
        modules_count=modules_count,
        topics_count=topics_count,
        duration=duration,
        course_type=check_course_type(course_name),
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_one_course(course) for course in courses]
