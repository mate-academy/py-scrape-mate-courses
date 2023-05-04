from selenium import webdriver
from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

MAIN_PAGE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    course_name = course_soup.select_one(".mb-16").text
    description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    return Course(
        name=course_name,
        short_description=description,
        course_type=CourseType.FULL_TIME
        if "Вечірній" not in course_name
        else CourseType.PART_TIME,
    )


def get_html_chosen_page(url: str = MAIN_PAGE_URL) -> str:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    driver.implicitly_wait(3)
    html = driver.page_source

    driver.quit()

    return html


def get_all_courses() -> list[Course]:
    html = get_html_chosen_page()

    soup = BeautifulSoup(html, "html.parser")
    courses = soup.find_all(
        "section", {"class": "CourseCard_cardContainer__7_4lK"}
    )

    return [parse_single_course(course) for course in courses]


if __name__ == "__main__":
    print(get_all_courses())
