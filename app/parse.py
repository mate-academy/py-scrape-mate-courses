from dataclasses import dataclass
from enum import Enum

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_one_course(course: WebElement, course_type: CourseType) -> Course:
    return Course(
        name=course.find_element(
            By.CLASS_NAME, "typography_landingH3__vTjok"
        ).text.split()[1],
        short_description=course.find_element(
            By.CLASS_NAME, "CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(HOME_URL)
    driver.execute_script("window.scrollBy(0, 1000)")
    all_courses = []
    for course_type in ("full-time", "part-time"):
        course_type_info = driver.find_element(By.ID, course_type)
        courses = course_type_info.find_elements(
            By.CLASS_NAME, "CourseCard_cardContainer__7_4lK"
        )
        course_type = (
            CourseType.FULL_TIME
            if course_type == "full-time"
            else CourseType.PART_TIME
        )
        all_courses.extend(
            [parse_one_course(course, course_type) for course in courses]
        )
    return all_courses


if __name__ == "__main__":
    print(get_all_courses())
