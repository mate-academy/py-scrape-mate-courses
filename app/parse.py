from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

MATE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_of_modules: int
    num_of_topics: int
    duration: str


def course_additional_info(url: str, course_type: CourseType) -> tuple:
    course_page = requests.get(urljoin(MATE_URL, url)).content
    soup = BeautifulSoup(course_page, "html.parser")

    num_of_modules = int(
        soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP"
        ).text.split()[0]
    )
    num_of_topics = int(
        soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR"
        ).text.split()[0]
    )
    if course_type == CourseType.FULL_TIME:
        duration = soup.select_one(
            ".FullTimeCourseScheduleSection_courseDuration__ebGIv"
        ).text
    else:
        duration = "Personal Schedule"
    return num_of_modules, num_of_topics, duration


def parse_course(course_soup: Tag, course_type: CourseType) -> Course:
    modules, topics, duration = course_additional_info(
        url=course_soup.select_one("a")["href"], course_type=course_type
    )
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=course_type,
        num_of_modules=modules,
        num_of_topics=topics,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_soup = soup.select("#full-time .CourseCard_cardContainer__7_4lK")
    part_time_soup = soup.select("#part-time .CourseCard_cardContainer__7_4lK")

    full_time_courses = [
        parse_course(course, CourseType.FULL_TIME) for course in full_time_soup
    ]

    part_time_courses = [
        parse_course(course, CourseType.PART_TIME) for course in part_time_soup
    ]

    all_courses = full_time_courses + part_time_courses

    return all_courses


if __name__ == "__main__":
    get_all_courses()
