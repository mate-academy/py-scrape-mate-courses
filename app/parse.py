from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup


BASE_RUL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def check_course_type(course: BeautifulSoup) -> CourseType:
    if course.select_one(
            ".typography_landingH3__vTjok"
    ).text.split()[-1] == "Вечірній":
        return CourseType.PART_TIME
    else:
        return CourseType.FULL_TIME


def parse_one_course(course: BeautifulSoup) -> Course:
    course_type = check_course_type(course)

    return Course(
        name=course.select_one(
            ".typography_landingH3__vTjok"
        ).text,
        short_description=course.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_RUL).content
    soup = BeautifulSoup(response, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_one_course(course) for course in courses]


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
