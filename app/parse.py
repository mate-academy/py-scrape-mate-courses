from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

from bs4 import BeautifulSoup

import requests

MATE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(page_soup: BeautifulSoup) -> Course:
    name = page_soup.select_one(".typography_landingH3__vTjok").text
    short_description = page_soup.select_one(
        ".CourseCard_flexContainer__dJk4p").text
    course_type = CourseType.PART_TIME if "Вечірній" in name \
        else CourseType.FULL_TIME
    return Course(name, short_description, course_type)


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_single_course(course) for course in courses]


@dataclass
class DetailCourse:
    modules: str
    topics: str
    duration: str
    course_type: CourseType


def get_detail_course_info(course_name: str) -> DetailCourse:
    """course_name ex. python/python-parttime"""
    detail_url = urljoin(MATE_URL, "courses/" + course_name)
    detail_page = requests.get(detail_url).content
    soup = BeautifulSoup(detail_page, "html.parser")
    moduls = soup.select_one(".CourseModulesHeading_modulesNumber__GNdFP").text
    topics = soup.select_one(".CourseModulesHeading_topicsNumber__PXMnR").text
    if "parttime" in course_name:
        course_type = CourseType.PART_TIME
        duration = "Personal plan"
    else:
        course_type = CourseType.FULL_TIME
        duration = soup.select_one(
            ".FullTimeCourseScheduleSection_durationWrapper__1vVot"
        ).text
    return DetailCourse(moduls, topics, duration, course_type.value)


if __name__ == "__main__":
    print(get_all_courses())
