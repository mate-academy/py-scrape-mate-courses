from dataclasses import dataclass
import time
from enum import Enum
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

URL = "https://mate.academy/"


driver: WebDriver | None = None


def get_driver() -> WebDriver:
    return _driver


def set_driver(new_driver: WebDriver) -> None:
    global _driver
    _driver = new_driver


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


def parse_single_course(course: WebElement) -> Course:
    new_url = course.find_element(By.TAG_NAME, "a").get_attribute("href")
    request = requests.get(new_url).content
    soup = BeautifulSoup(request, "html.parser")
    try:
        duration = soup.select_one(
            "div.CourseModulesHeading_courseDuration__f_c3H > p"
        ).text
    except AttributeError:
        duration = None
    return Course(
        name=course.find_element(
            By.CLASS_NAME, "typography_landingH3__vTjok"
        ).text,
        short_description=course.find_element(
            By.CLASS_NAME, "CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=CourseType.PART_TIME
        if new_url.split("-")[-1] == "parttime"
        else CourseType.FULL_TIME,
        modules=int(
            soup.select_one(
                "div.CourseModulesHeading_modulesNumber__GNdFP > p"
            ).text.split()[0]
        ),
        topics=int(
            soup.select_one(
                "div.CourseModulesHeading_topicsNumber__PXMnR > p"
            ).text.split()[0]
        ),
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    with webdriver.Chrome() as new_drier:
        set_driver(new_drier)
        _driver.get(URL)
        time.sleep(5)
        courses = _driver.find_elements(
            By.CLASS_NAME, "CourseCard_cardContainer__7_4lK"
        )
        return [parse_single_course(course) for course in courses]
