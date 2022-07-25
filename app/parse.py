import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def get_single_course(course, course_type: CourseType):
    return Course(
            name=course.select_one("span.typography_landingH3__vTjok")
            .text.replace("Курс ", "")
            .replace(" Вечірній", ""),
            short_description=course.select_one("p").text,
            type=course_type

        )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    result = []
    for course_type in CourseType:
        course_block = soup.select_one(f"#{course_type.value}")
        courses = course_block.select("section.CourseCard_cardContainer__7_4lK")
        for course in courses:
            result.append(get_single_course(course, course_type))

    return result


def main():
    print(get_all_courses())


if __name__ == '__main__':
    main()
