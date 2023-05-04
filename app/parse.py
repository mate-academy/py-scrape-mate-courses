from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import requests

PARSE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def study_format(course_soup: BeautifulSoup) -> bool:
    value = course_soup.select_one(
        ".typography_landingH3__vTjok"
    ).text.split()[-1]

    return value == "Вечірній"


def parse_simple_cource(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=CourseType.PART_TIME if study_format(
            course_soup) else CourseType.FULL_TIME
    )


def get_all_courses() -> list[Course]:
    service = Service("/usr/local/bin/chromedriver")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(PARSE_URL)

    WebDriverWait(driver, 10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    course_soup = soup.find_all(class_="CourseCard_cardContainer__7_4lK")

    res = [parse_simple_cource(course) for course in course_soup]
    driver.quit()

    return res
