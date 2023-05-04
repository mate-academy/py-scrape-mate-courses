import time

from dataclasses import dataclass
from enum import Enum
from selenium import webdriver
from bs4 import BeautifulSoup
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


def pars_single_course(course: BeautifulSoup) -> Course:
    single_course = Course(
        name=course.select_one(".typography_landingH3__vTjok").text,
        short_description=course.select_one("p").text,
        course_type=CourseType.FULL_TIME if
        "full-time" in course.parent.parent.attrs["id"]
        else CourseType.PART_TIME
    )
    print(single_course)
    return single_course


def get_all_courses() -> list[Course]:
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    driver.get(BASE_URL)
    time.sleep(1)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    courses_list = soup.find_all(
        "section",
        class_="CourseCard_cardContainer__7_4lK"
    )

    print(len(courses_list))
    return [pars_single_course(course) for course in courses_list]


if __name__ == "__main__":
    get_all_courses()
