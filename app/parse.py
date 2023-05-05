from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def load_page(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector("#part-time .typography_landingH3__vTjok")
        content = page.content()
        browser.close()
    return content


def get_course_type(name: str) -> CourseType:
    if "Вечірній" in name:
        return CourseType.PART_TIME

    return CourseType.FULL_TIME


def parse_single_course(course: BeautifulSoup) -> Course:
    name = course.select_one(".typography_landingH3__vTjok").text
    short_description = course.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = get_course_type(name)

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = load_page(BASE_URL)
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in courses]
