from dataclasses import dataclass
from enum import Enum

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


def parse_single_course(course_soup: BeautifulSoup, time: str) -> Course:
    if time == CourseType.FULL_TIME:
        return Course(
            name=course_soup.select_one(".typography_landingH3__vTjok").text,
            short_description=course_soup.select_one(
                ".CourseCard_courseDescription__Unsqj"
            ).text,
            course_type=time,
        )
    return Course(
        name=course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text + " Вечірній",
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=time,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    times = [CourseType.FULL_TIME, CourseType.PART_TIME]
    result = []
    for time in times:
        courses_list_time = [
            parse_single_course(course_soup, time)
            for course_soup in courses
        ]
        result += courses_list_time
        print(result)
    return result
