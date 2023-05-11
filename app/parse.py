from selenium import webdriver
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_driver() -> webdriver:
    service = Service("/usr/local/bin/chromedriver")
    options = Options().add_argument("--headless")
    return webdriver.Chrome(
        service=service,
        options=options,
        executable_path="chromedriver-path"
    )


def close_driver(driver: webdriver) -> None:
    driver.quit()


def get_courses(driver: webdriver, course_type: CourseType) -> list[Course]:
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    courses_list = []
    courses = soup.find("div", {"id": course_type.value})
    courses = courses.find_all(
        "section", {"class": "CourseCard_cardContainer__7_4lK"}
    )
    for course in courses:
        title = course.find(
            "span", {"class": "typography_landingH3__vTjok"}
        ).text
        description = course.find(
            "p",
            {
                "class": "typography_landingMainText__Ux18x "
                         "CourseCard_courseDescription__Unsqj"
            },
        ).text
        course = Course(
            name=title, short_description=description, course_type=course_type
        )
        courses_list.append(course)
    return courses_list


def get_all_courses() -> list[Course]:
    driver = get_driver()
    all_courses = []
    all_courses.extend(get_courses(driver, CourseType.FULL_TIME))
    all_courses.extend(get_courses(driver, CourseType.PART_TIME))
    close_driver(driver)
    return all_courses
