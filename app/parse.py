from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(data: Tag) -> Course:
    name = data.select_one(".typography_landingH3__vTjok").text
    short_description = data.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = (
        CourseType.PART_TIME if "Вечірній" in name else CourseType.FULL_TIME
    )

    return Course(
        name=name, short_description=short_description, course_type=course_type
    )


def get_page_source(url: str) -> str:
    options = Options()
    options.add_argument("--headless")
    chrome = webdriver.Chrome(
        options=options, executable_path="chromedriver-path"
    )
    chrome.get(url)
    chrome.implicitly_wait(10)

    page_source = chrome.page_source
    chrome.quit()

    return page_source


def parse_courses_from_page(page_source: str) -> list[Course]:
    soup = BeautifulSoup(page_source, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in courses]


def get_all_courses() -> list[Course]:
    page_source = get_page_source(URL)
    courses = parse_courses_from_page(page_source)

    return courses


if __name__ == "__main__":
    print(get_all_courses())
