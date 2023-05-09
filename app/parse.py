import time
from dataclasses import dataclass
from enum import Enum


import requests
from bs4 import BeautifulSoup, Tag

from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def set_up_chrome_driver() -> webdriver:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    return driver


URL = "https://mate.academy"


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
    duration: str | None


def get_single_course(course: Tag) -> Course:
    course_type = course.parent.parent.get("id")
    print(course_type)
    if course_type == CourseType.FULL_TIME.value:
        course_type = CourseType.FULL_TIME
    else:
        course_type = CourseType.PART_TIME

    name = course.select_one(
        ".typography_landingH3__vTjok"
    ).text.split(" ")[1]

    description = course.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text

    link_to_detail_page = course.select_one(
        ".CourseCard_button__HTQvE"
    )["href"]

    response = requests.get(URL + link_to_detail_page)
    soup = BeautifulSoup(response.content, "html.parser")
    course_info = soup.select(
        ".typography_landingMainText__Ux18x.CourseModulesHeading_text__EdrEk"
    )
    modules, topics = [info.text.split(" ")[0] for info in course_info[:2]]
    duration = course_info[2].text if len(course_info) == 3 else None

    course = Course(
        name=name,
        course_type=course_type,
        short_description=description,
        modules=modules,
        topics=topics,
        duration=duration
    )

    return course


def get_all_courses() -> list[Course]:
    with set_up_chrome_driver() as driver:
        driver.get(URL)
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_single_course(course) for course in courses]


if __name__ == "__main__":
    get_all_courses()
