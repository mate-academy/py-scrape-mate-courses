from dataclasses import dataclass
from enum import Enum
from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag, ResultSet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    description: str
    course_type: CourseType


def get_detail_course_page(course_soup: BeautifulSoup) -> BeautifulSoup:
    href = course_soup.select_one(".mb-16")["href"]
    html = requests.get(BASE_URL + href).content
    course_detail_page_soup = BeautifulSoup(html, "html.parser")

    return course_detail_page_soup


def parse_course(course_soup: BeautifulSoup) -> Course:
    course_name = course_soup.select_one(".mb-16").text
    description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text

    return Course(
        name=course_name,
        description=description,
        course_type=CourseType.PART_TIME
        if "Вечір" in course_name
        else CourseType.FULL_TIME,
    )


def get_html_chosen_page(url: str = BASE_URL) -> str:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(1)
    html = driver.page_source
    driver.quit()

    return html


def get_all_courses() -> list[Course]:
    html = get_html_chosen_page()
    soup = BeautifulSoup(html, "html.parser")
    courses = soup.find_all(
        "section", {"class": "CourseCard_cardContainer__7_4lK"}
    )

    return [parse_course(course) for course in courses]


print(get_all_courses())
