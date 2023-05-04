import requests
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
    modules: int
    topics: int
    duration: str


def get_detail_course_page(course_soup: BeautifulSoup) -> str:
    href = course_soup.select_one(".mb-16")["href"]
    html = requests.get(MAIN_PAGE_URL + href).content

    soup = BeautifulSoup(html, "html.parser")

    return soup


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    course_name = course_soup.select_one(".mb-16").text
    description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    detail_soup = get_detail_course_page(course_soup)
    modules = detail_soup.select_one(
        "div.CourseModulesHeading_modulesNumber__GNdFP >"
        " p.CourseModulesHeading_text__EdrEk"
    ).text.split()[0]
    topics = detail_soup.select_one(
        "div.CourseModulesHeading_topicsNumber__PXMnR >"
        " p.CourseModulesHeading_text__EdrEk"
    ).text.split()[0]
    duration = detail_soup.select_one(
        "div.CourseModulesHeading_courseDuration__f_c3H >"
        " p.CourseModulesHeading_text__EdrEk"
    )
    return Course(
        name=course_name,
        short_description=description,
        course_type=CourseType.FULL_TIME
        if "Вечірній" not in course_name
        else CourseType.PART_TIME,
        modules=int(modules),
        topics=int(topics),
        duration=duration.text if duration else None,
    )


def get_html_chosen_page(url: str = MAIN_PAGE_URL) -> str:
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

    return [parse_single_course(course) for course in courses]


if __name__ == "__main__":
    print(get_all_courses())
