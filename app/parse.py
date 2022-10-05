from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"
COURSES_SELECTOR = ".CourseCard_cardContainer__7_4lK"
COURSE_NAME_SELECTOR = ".typography_landingH3__vTjok"
COURSE_DESCRIPTION_SELECTOR = ".CourseCard_courseDescription__Unsqj"
COURSE_ADDITIONAL_INFO_SELECTOR = ".CourseModulesHeading_headingGrid__50qAP"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    learning_type: CourseType
    count_of_modules: str
    count_of_topics: str
    duration: str


def get_additional_info(url: str) -> [BeautifulSoup]:
    course_url = urljoin(BASE_URL, url)
    course_page = requests.get(course_url).content
    soup = BeautifulSoup(course_page, "html.parser")
    course_info = soup.select_one(COURSE_ADDITIONAL_INFO_SELECTOR)

    return [info.p.text for info in course_info]


def parse_single_course(course_soup: BeautifulSoup) -> [Course]:
    additional_info = get_additional_info(course_soup.a["href"])
    return Course(
        name=course_soup.select_one(COURSE_NAME_SELECTOR).text,
        short_description=course_soup.select_one(
            COURSE_DESCRIPTION_SELECTOR
        ).text.strip(),
        learning_type=CourseType.PART_TIME
        if course_soup.select_one("[rel=nofollow]")
        else CourseType.FULL_TIME,
        count_of_modules=additional_info[0],
        count_of_topics=additional_info[1],
        duration=additional_info[2]
        if len(additional_info) > 2 else None
    )


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    all_courses = soup.select(COURSES_SELECTOR)

    return [parse_single_course(course) for course in all_courses]
