from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

MATE_URL = "https://mate.academy/ru"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_singe_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = (
        CourseType.FULL_TIME if "Вечерний" in name else CourseType.PART_TIME
    )
    return Course(name, short_description, course_type)


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_singe_course(course) for course in courses]


@dataclass
class DetailCourse:
    course_name: str
    course_type: CourseType
    moduls: str
    topic: str
    duration: str

    def __str__(self) -> str:
        return f"{self.course_name}, {self.course_type}," \
               f" {self.moduls}, {self.topic}, {self.duration}"


def detail_course_info(course: str)\
        -> DetailCourse:  # name of course ex. python or python-parttime
    detail_url = urljoin(MATE_URL, "courses/" + course)
    detail_page = requests.get(detail_url).content
    soup = BeautifulSoup(detail_page, "html.parser")
    moduls = soup.select_one(".CourseModulesHeading_modulesNumber__GNdFP").text
    topic = soup.select_one(".CourseModulesHeading_topicsNumber__PXMnR").text
    if "parttime" not in course:
        course_type = CourseType.FULL_TIME
        duration = soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H"
        ).text
    else:
        course_type = CourseType.PART_TIME
        duration = "Personal plan"
    return DetailCourse(course, course_type.value, moduls, topic, duration)
