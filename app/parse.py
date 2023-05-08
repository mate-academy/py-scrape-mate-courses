from dataclasses import dataclass, fields
from enum import Enum
from typing import List

from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


def get_course_type(name: str) -> CourseType:
    if "Вечірній" in name:
        return CourseType.PART_TIME
    return CourseType.FULL_TIME


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


Course_FIELDS: List[str] = [field.name for field in fields(Course)]


def parse_single_course(course: Tag) -> Course:
    name = course.find_element(
        By.CSS_SELECTOR,
        ".typography_landingH3__vTjok"
    ).text
    return Course(
        name=name,
        short_description=course.find_element(
            By.CSS_SELECTOR,
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=get_course_type(name)
    )


def get_all_courses() -> list[Course]:
    options = Options()
    options.headless = True
    service = Service("path/to/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.presence_of_element_located((
        By.CSS_SELECTOR,
        ".CourseCard_cardContainer__7_4lK"
    )))
    courses = driver.find_elements(
        By.CSS_SELECTOR,
        ".CourseCard_cardContainer__7_4lK"
    )
    result = []
    for course in courses:
        result.append(parse_single_course(course))
    driver.quit()
    return result
