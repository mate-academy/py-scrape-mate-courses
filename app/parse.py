from dataclasses import dataclass
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_all_courses() -> list[Course]:
    parser = CoursesParser()

    return parser.parse()


class CoursesParser:
    TYPE_OF_COURSES = {
        "#full-time": CourseType.FULL_TIME,
        "#part-time": CourseType.PART_TIME,
    }
    URL = "https://mate.academy/"

    def __init__(self) -> None:
        self.courses = []

    def parse(self) -> List[Course]:
        response = requests.get(CoursesParser.URL).content
        soup = BeautifulSoup(response, "html.parser")

        print(self.__parse_data(soup, "#full-time"))
        print(self.__parse_data(soup, "#part-time"))

        return self.courses

    def __parse_data(
            self,
            soup: BeautifulSoup,
            specific_course: str
    ) -> None:
        data = soup.select_one(specific_course)
        courses_content = data.select(".CourseCard_cardContainer__7_4lK")

        for course_content in courses_content:

            self.courses.append(
                self.__initialize_course_instance(
                    name=course_content.select_one(".mb-16 > span").text,
                    short_description=course_content.select_one(
                        ".CourseCard_flexContainer__dJk4p > p"
                    ).text,
                    specific_course=specific_course
                )
            )

    def __initialize_course_instance(
            self,
            name: str,
            short_description: str,
            specific_course: str
    ) -> Course:
        return Course(
            name=name,
            short_description=short_description,
            course_type=CoursesParser.TYPE_OF_COURSES[specific_course]
        )
