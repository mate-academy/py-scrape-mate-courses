import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass
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


def parse_page() -> BeautifulSoup:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    course_soup = soup.select("div[class*=ProfessionCard_card]")
    return course_soup


def get_single_course(course_soup: BeautifulSoup) -> [Course]:
    courses = []

    name = course_soup.select_one("a[class*=ProfessionCard_title]").text
    short_description = course_soup.select_one(".mb-32").text
    part_time = course_soup.select_one("a[class*=Button_secondary]")
    full_time = course_soup.select_one("a[class*=Button_primary]")

    if part_time:
        courses.append(Course(name, short_description, CourseType.PART_TIME))
    if full_time:
        courses.append(Course(name, short_description, CourseType.FULL_TIME))
    return courses


def get_all_courses() -> list[Course]:
    all_courses = []
    course_soup = parse_page()

    for course in course_soup:
        all_courses.extend(get_single_course(course))

    return all_courses
