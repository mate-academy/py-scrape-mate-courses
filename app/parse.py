import logging
import sys
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    topics: int
    duration: str


def get_course_absolute_url(base_url: str, course_tag: Tag) -> str:
    course_url = course_tag.select_one("section > a[href]")["href"]

    return urljoin(base_url, course_url)


def get_course_info(url: str) -> dict:
    web_page = requests.get(url).content
    soup = BeautifulSoup(web_page, "html.parser")

    modules = soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).string
    topics = soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).string
    duration = soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H"
    )

    return dict(
        modules=int(modules.split()[0]),
        topics=int(topics.split()[0]),
        duration=duration.string if duration else "Own study schedule"
    )


def parse_single_course(
        course_type: CourseType,
        course_tag: Tag
) -> Course:
    course_url = get_course_absolute_url(BASE_URL, course_tag)
    course_info = get_course_info(course_url)

    course = Course(
        name=course_tag.select_one(".typography_landingH3__vTjok").string,
        short_description=course_tag.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).string,
        course_type=course_type,
        modules=course_info["modules"],
        topics=course_info["topics"],
        duration=course_info["duration"]
    )
    logging.info(f"Course '{course.name}' was parsed")

    return course


def get_course_type_with_courses(
        course_type: CourseType,
        courses_soup: BeautifulSoup
) -> list[Course]:
    course_tags = courses_soup.select(
        f"#{course_type.value} .CourseCard_cardContainer__7_4lK"
    )

    return [
        parse_single_course(course_type, course)
        for course in course_tags
    ]


def get_all_courses() -> list[Course]:
    web_page = requests.get(BASE_URL).content
    soup = BeautifulSoup(web_page, "html.parser")
    courses = list()

    for course_type in CourseType:
        courses.extend(
            get_course_type_with_courses(course_type, soup)
        )

    return courses
