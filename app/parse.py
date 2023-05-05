from dataclasses import dataclass
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup, Tag

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: Tag) -> [Course]:
    name = (course_soup.select_one(".typography_landingH3__vTjok").text, )[0]
    short_description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = CourseType.FULL_TIME
    if "Вечірній" in name:
        course_type = CourseType.PART_TIME

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(HOME_URL)
    driver.implicitly_wait(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
