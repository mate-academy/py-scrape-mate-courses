from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = (
    "https://mate.academy/"
    "?utm_source=google&utm_medium=cpc&utm_term"
    "=мейт%20академи&utm_content=659738950077"
    "&utm_campaign=gs_brand_exp&gad=1&gclid=Cj0KCQjwmtGjBhDhARIsAEqfDEeKg"
    "-CJteM5sYqSWO44MKUUv4yJ1UaJNZLqe1QOVuScc01xNucKUVkaAgV8EALw_wcB"
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_home_page() -> BeautifulSoup:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    soup.get("[id=all-courses]")
    return soup


def get_full_time_courses(soup: BeautifulSoup) -> list[Course]:
    current_course = soup.find("div", id="full-time")
    all_full_time_course = current_course.select("section")
    return [
        Course(
            name=course.select_one("a > span").text,
            short_description=course.select_one("section > div > p").text,
            course_type=CourseType("full-time"),
        )
        for course in all_full_time_course
    ]


def get_part_time_courses(soup: BeautifulSoup) -> list[Course]:
    current_course = soup.find("div", id="part-time")
    all_part_time_course = current_course.select("section")
    return [
        Course(
            name=course.select_one("a > span").text,
            short_description=course.select_one("section > div > p").text,
            course_type=CourseType("part-time"),
        )
        for course in all_part_time_course
    ]


def get_all_courses() -> list[Course]:
    soup = get_home_page()
    return [
        *get_part_time_courses(soup),
        *get_full_time_courses(soup)
    ]


if __name__ == "__main__":
    get_all_courses()
