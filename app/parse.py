from typing import Type

import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, ResultSet, Tag

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType

    @classmethod
    def create_single_course(
            cls: Type["Course"],
            name: str,
            short_description: str,
            course_type: CourseType
    ) -> "Course":
        return cls(name, short_description, course_type)


def get_page() -> bytes:
    return requests.get(BASE_URL).content


def get_page_soup() -> BeautifulSoup:
    return BeautifulSoup(get_page(), "html.parser")


def get_all_courses_soup() -> ResultSet[Tag]:
    return get_page_soup().select(".ProfessionCard_cardWrapper__JQBNJ")


def get_all_courses() -> list[Course]:
    courses_soup = get_all_courses_soup()
    courses_list = []

    for course in courses_soup:
        course_name = course.a.string
        short_description = (
            course.select_one(
                ".typography_landingTextMain__Rc8BD.mb-32"
            ).get_text()
        )
        course_types = course.find_all(
            "span", class_="ButtonBody_buttonText__FMZEg"
        )

        for course_type in course_types:
            course_type_text = course_type.get_text()
            course_type_enum = (
                CourseType.FULL_TIME
                if course_type_text == "Повний день"
                else CourseType.PART_TIME
            )

            courses_list.append(Course.create_single_course(
                course_name,
                short_description,
                course_type_enum
            ))

    return courses_list


if __name__ == "__main__":
    get_all_courses()
