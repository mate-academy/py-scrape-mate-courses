from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

HOME_URL = "https://mate.academy/en/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_course_info(course_section: Tag, course_type: CourseType) -> Course:
    name = course_section.find(class_="typography_landingH3__vTjok").text
    short_description = course_section.find(
        class_="typography_landingP1__N9PXd").text

    return Course(name, short_description, course_type)


def get_courses_by_type(course_type: CourseType) -> list[Course]:
    response = requests.get(HOME_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    course_sections = soup.find(
        id=course_type.value
    ).find_all(class_="CourseCard_cardContainer__7_4lK")

    return [get_course_info(
        course_section, course_type) for course_section in course_sections]


def get_all_courses() -> list[Course]:
    all_courses = []

    for course_type in CourseType:
        all_courses.extend(get_courses_by_type(course_type))

    return all_courses


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
