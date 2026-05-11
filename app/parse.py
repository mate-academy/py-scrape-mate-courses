from dataclasses import dataclass

import requests
from bs4 import Tag, BeautifulSoup

BASE_URL = "https://mate.academy"
COURSES_URL = "https://mate.academy/#all-courses"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one("[class*='ProfessionCard_title']").text,
        short_description=course.select_one(
            "[class*='ProfessionCard_description']"
        ).text,
        duration=course.select_one("[class*='ProfessionCard_duration']").text
    )


def get_course_page(soup: Tag) -> list[Course]:
    courses = soup.select(".ProfessionCard_content__mPiVi")
    return [parse_single_course(course) for course in courses]


def get_all_courses() -> list[Course]:
    text = requests.get(COURSES_URL).content
    soup = BeautifulSoup(text, features="html.parser")

    return get_course_page(soup)
