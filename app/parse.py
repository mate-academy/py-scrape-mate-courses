import logging
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from dataclasses import dataclass
from enum import Enum


BASE_URL = "https://mate.academy/"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:
    course = Course(
        name=course_soup.select_one("a", {"class": "mb-16"}).text,
        short_description=(
            course_soup.select_one(
                "p", {"class": "typography_"}, partial=True).text
        ),
        course_type=course_type
    )
    logging.info(f"Course '{course.name}' was parsed")
    return course


def get_all_courses() -> list[Course]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        "/usr/lib/chromium-browser/chromedriver",
        options=chrome_options
    )
    driver.get(BASE_URL)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    courses_list = []

    for course_type in CourseType:
        section = soup.find("div", {"id": course_type.value})
        courses = section.findAll(
            "section", {"class": "CourseCard_cardContainer__7_4lK"}
        )

        for course in courses:
            courses_list.append(parse_single_course(course, course_type))

    return courses_list


def main() -> None:
    print(get_all_courses())


if __name__ == "__main__":
    main()
