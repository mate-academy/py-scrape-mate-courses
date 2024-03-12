from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: BeautifulSoup,
                        ) -> list[Course]:
    courses = []

    button_texts = [
        button.text
        for button in course_soup.select(".ButtonBody_buttonText__FMZEg")
    ]
    if "Full time" in button_texts:
        append_course(course_soup, courses, CourseType.FULL_TIME)
    if "Flex" in button_texts:
        append_course(course_soup, courses, CourseType.PART_TIME)
    return courses


def append_course(course_soup: BeautifulSoup,
                  courses: list[Course],
                  type_of_course: CourseType,
                  ) -> None:
    courses.append(
        Course(
            name=course_soup.select_one("h3").text,
            short_description=course_soup.select(
                ".typography_landingTextMain__Rc8BD"
            )[-1].text,
            course_type=type_of_course,
        )
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course_soup in courses_soup:
        all_courses.extend(parse_single_course(course_soup))

    return all_courses


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
