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


class Parsing:
    def __init__(self) -> None:
        self.result = []

    def parse_course(self, course: BeautifulSoup, course_type: str) -> Course:
        return Course(
            name=course.select_one(".typography_landingH3__vTjok").text[5:],
            short_description=course.select_one(
                ".CourseCard_courseDescription__Unsqj"
            ).text,
            course_type=CourseType(course_type)
        )

    def get_all_course_one_type(
        self,
        parsed_page: BeautifulSoup,
        selector: str,
        course_type: str
    ) -> list[Course]:
        courses = parsed_page.select(f"{selector}")
        return [self.parse_course(course, course_type) for course in courses]

    def get_all_courses(self) -> list[Course]:
        parsed_page = requests.get(BASE_URL).content
        page_soup = BeautifulSoup(parsed_page, "html.parser")
        full_time = self.get_all_course_one_type(
            page_soup,
            "#full-time > div > section.CourseCard_cardContainer__7_4lK",
            "full-time"
        )
        part_time = self.get_all_course_one_type(
            page_soup,
            "#part-time > div > section.CourseCard_cardContainer__7_4lK",
            "part-time"
        )
        self.result.extend(full_time)
        self.result.extend(part_time)

        return self.result
