from dataclasses import dataclass
from enum import Enum
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"
NAME = ".typography_landingH3__vTjok"
DESCRIPTION = ".CourseCard_courseDescription__Unsqj"
ADDITIONAL_INFO = ".CourseModulesHeading_headingGrid__50qAP"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    count_of_modules: str
    count_of_topics: str
    duration: str


def get_additional_info(url):
    course_url = urljoin(BASE_URL, url)
    course_page = requests.get(course_url).content
    soup = BeautifulSoup(course_page, "html.parser")
    course_info = soup.select_one(ADDITIONAL_INFO)

    return [info.p.text for info in course_info]


def parse_single_course(course_soup: BeautifulSoup) -> [Course]:
    additional_info = get_additional_info(course_soup.a["href"])
    return Course(
        name=course_soup.select_one(NAME).text,
        short_description=course_soup.select_one(DESCRIPTION).text.strip(),
        type=CourseType.PART_TIME if course_soup.select_one("[rel=nofollow]")
        else CourseType.FULL_TIME,
        count_of_modules=additional_info[0],
        count_of_topics=additional_info[1],
        duration=additional_info[2]
        if len(additional_info) > 2 else None
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    all_courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in all_courses]
