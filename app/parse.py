from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

COURSES_URL = "https://mate.academy/"
service = Service("/usr/local/bin/chromedriver")
options = Options()
options.add_argument("--headless")
DRIVER = webdriver.Chrome(service=service, options=options)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_one_course(item: Tag) -> Course:
    name = item.select_one(".typography_landingH3__vTjok").text
    course_type = (CourseType.PART_TIME
                   if "Вечірній" in name
                   else CourseType.FULL_TIME)
    return Course(
        name=name,
        short_description=item.select_one(
            ".typography_landingMainText__Ux18x"
        ).text,
        course_type=course_type)


def get_page_data(selector: str, driver: WebDriver) -> Iterable:
    driver.get(COURSES_URL)
    source = BeautifulSoup(driver.page_source, "html.parser")
    courses = source.select(selector)
    driver.quit()
    return courses


def get_all_courses() -> list[Course]:
    courses = get_page_data(".CourseCard_cardContainer__7_4lK", DRIVER)

    return [parse_one_course(course) for course in courses]
