from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_modules: str
    num_topics: str
    months_duration: str


def parse_single_course(course_soup: Tag, course_type: CourseType) -> Course:
    detail_href = course_soup.select_one("a.CourseCard_button__HTQvE").get(
        "href"
    )
    detail_page = requests.get(urljoin(BASE_URL, detail_href)).content
    detail_soup = BeautifulSoup(detail_page, "html.parser")

    duration_elem = detail_soup.select_one("div.CourseModulesHeading_courseDuration__f_c3H")
    months_duration = duration_elem.text if duration_elem is not None else None

    return Course(
        name=course_soup.select_one("span.typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            "p.CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
        num_modules=detail_soup.select_one(
            "div.CourseModulesHeading_modulesNumber__GNdFP"
        ).text,
        num_topics=detail_soup.select_one(
            "div.CourseModulesHeading_topicsNumber__PXMnR"
        ).text,
        months_duration=months_duration,
    )


def get_courses_by_type(course_type: CourseType) -> list[Course]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    service = Service("/usr/lib/chromium-browser/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(BASE_URL)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(f"#{course_type.value} section")

    return [
        parse_single_course(course_soup, course_type)
        for course_soup in courses_soup
    ]


def get_all_courses() -> list[Course]:
    return [
        *get_courses_by_type(CourseType.FULL_TIME),
        *get_courses_by_type(CourseType.PART_TIME),
    ]


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
