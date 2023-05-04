from typing import List

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup, Tag, ResultSet
from dataclasses import dataclass
from enum import Enum

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        name: str,
        description: str,
        course_type: CourseType
) -> Course:
    return Course(
        name=name,
        short_description=description,
        course_type=course_type
    )


def parse_full_time_courses(full_time_soup: ResultSet[Tag]) -> List[Course]:
    names = [course.select_one(
        ".mb-16 span"
    ).text for course in full_time_soup]
    descriptions = [
        course.select_one(
            ".CourseCard_flexContainer__dJk4p p"
        ).text for course in full_time_soup
    ]

    courses = []
    for name, description in zip(names, descriptions):
        course_type = CourseType.FULL_TIME if len(
            name.split()
        ) < 3 else CourseType.PART_TIME
        course = parse_single_course(name.split()[1], description, course_type)
        courses.append(course)

    return courses


def parse_all_courses(page_soup: BeautifulSoup) -> List[Course]:
    course_soup = page_soup.select("section .CourseCard_cardContainer__7_4lK")
    courses = parse_full_time_courses(course_soup)
    return courses


def get_all_courses() -> List[Course]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        "/usr/lib/chromium-browser/chromedriver",
        options=chrome_options
    )
    driver.get(HOME_URL)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    courses = parse_all_courses(soup)
    driver.quit()

    return courses
