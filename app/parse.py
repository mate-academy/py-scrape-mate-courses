import requests

from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, Tag, ResultSet


BASE_URL = "https://mate.academy/"
DETAIL_URL = BASE_URL + "courses/{course_name}"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_page(url: str, selector: str) -> ResultSet[Tag]:
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html.parser")
    return soup.select(selector)


def get_course(course: Tag) -> Course:
    course = Course(
        name=course.select_one(".typography_landingH3__vTjok").text,
        short_description=course.select_one(
            ".CourseCard_flexContainer__dJk4p p"
        ).text,
        course_type=CourseType.FULL_TIME,
    )

    if course.name.endswith("Вечірній"):
        course.course_type = CourseType.PART_TIME

    return course


def get_all_courses() -> list[Course]:
    main_page = get_page(BASE_URL, ".CourseCard_cardContainer__7_4lK")
    return [get_course(course) for course in main_page]


if __name__ == "__main__":
    for i in get_all_courses():
        print(i)
