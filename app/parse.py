from dataclasses import dataclass
from enum import Enum

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_course(course: WebElement, course_type: CourseType) -> Course:
    return Course(
        name=course.find_element(
            By.CLASS_NAME, "typography_landingH3__vTjok"
        ).text,
        short_description=course.find_element(
            By.CLASS_NAME, "CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    driver = Chrome(ChromeDriverManager().install())
    driver.get(BASE_URL)

    full_time_courses = driver.find_element(By.ID, "full-time").find_elements(
        By.CLASS_NAME, "CourseCard_cardContainer__7_4lK"
    )
    part_time_courses = driver.find_element(By.ID, "part-time").find_elements(
        By.CLASS_NAME, "CourseCard_cardContainer__7_4lK"
    )

    courses = [
        parse_course(course, CourseType.FULL_TIME)
        for course in full_time_courses
    ] + [
        parse_course(course, CourseType.PART_TIME)
        for course in part_time_courses
    ]

    return courses
