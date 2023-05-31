from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests as requests
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
    module_count: int
    topic_count: int
    duration: str


def get_course_url(course_soup: BeautifulSoup) -> BeautifulSoup:
    course_url = course_soup.select_one("a").get("href", "")
    additional_url = urljoin(BASE_URL, course_url)
    page = requests.get(additional_url).content
    single_soup = BeautifulSoup(page, "html.parser")
    return single_soup


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one("a > span").text
    short_description = course_soup.select_one("div > p").text
    course_type = (
        CourseType.FULL_TIME
        if "Вечірній" not in name
        else CourseType.PART_TIME
    )

    single_soup = get_course_url(course_soup)

    module_count = int(
        single_soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP > p"
        ).text.split(" ")[0]
    )
    topic_count = int(
        single_soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR > p"
        ).text.split(" ")[0]
    )
    duration_element = single_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H > p"
    )
    duration = duration_element.text if duration_element else ""

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type,
        module_count=module_count,
        topic_count=topic_count,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]
