from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium import webdriver

from enum import Enum

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course: BeautifulSoup) -> Course:
    instance = Course(
        name=course.select_one("a > span").text,
        short_description=course.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=CourseType.FULL_TIME,
    )

    if "Вечірній" in instance.name:
        instance.course_type = CourseType.PART_TIME

    return instance


def get_all_courses() -> list[Course]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    all_courses = [
        parse_single_course(course)
        for course in courses
    ]
    return all_courses


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
