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
    course_type: CourseType
    modules_count: int
    topics_count: int
    duration: int


def create_course(
    name: str,
    short_description: str,
    course_type: CourseType,
    modules_count: int,
    topics_count: int,
    duration: int,
) -> Course:
    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type,
        modules_count=modules_count,
        topics_count=topics_count,
        duration=duration,
    )


def parse_course_page(course_link: str) -> list[int]:
    url = urljoin(BASE_URL, course_link[1:])
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")

    return [
        int(soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP"
        ).text.split()[0]),
        int(soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR"
        ).text.split()[0]),
        int(soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H"
        ).text.split()[0]),
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    courses = []

    for course_soup in courses_soup:
        name = course_soup.select_one(".ProfessionCard_title__Zq5ZY").text
        short_description = course_soup.select_one(".mb-32").text
        full_time = course_soup.select_one(".Button_primary__7fH0C")
        part_time = course_soup.select_one(".Button_secondary__DNIuD")

        if full_time:
            (
                modules_count,
                topics_count,
                duration,
            ) = parse_course_page(full_time["href"])

            courses.append(
                create_course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.FULL_TIME,
                    modules_count=modules_count,
                    topics_count=topics_count,
                    duration=duration,
                )
            )

        if part_time:
            (
                modules_count,
                topics_count,
                duration,
            ) = parse_course_page(part_time["href"])

            courses.append(
                create_course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.PART_TIME,
                    modules_count=modules_count,
                    topics_count=topics_count,
                    duration=duration,
                )
            )

    return courses
