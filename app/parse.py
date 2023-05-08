from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

from enum import Enum

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course: BeautifulSoup, course_type: str) -> Course:
    print(
        dict(
            name=course.select_one("a > span").text,
            short_description=course.select_one(
                "div.cell.large-6> section:nth-child(1) > div > p"
            ).text,
            course_type=course_type,
        )
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    full_time_courses = soup.select("#full-time")
    full_time = [
        parse_single_course(course, "full_time")
        for course in full_time_courses
    ]
    part_time_courses = soup.select("#part-time")
    part_time = [
        parse_single_course(course, "part_time")
        for course in part_time_courses
    ]
    return full_time + part_time


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
