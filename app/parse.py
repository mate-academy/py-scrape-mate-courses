from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(raw_data: Tag) -> Course:
    course_name = raw_data.select_one(".typography_landingH3__vTjok").text
    course_description = raw_data.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = (
        CourseType.PART_TIME
        if "вечірній" in course_name.lower()
        else CourseType.FULL_TIME
    )

    print(course_name, course_description, course_type)

    return Course(
        name=course_name,
        short_description=course_description,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    options = Options()
    options.add_argument("--headless")
    chrome = webdriver.Chrome(
        options=options,
        executable_path="chromedriver-path",
    )
    chrome.get(URL)

    chrome.implicitly_wait(20)

    soup = BeautifulSoup(chrome.page_source, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_single_course(course) for course in courses]


if __name__ == "__main__":
    get_all_courses()
