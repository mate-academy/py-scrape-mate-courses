from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_course_detail(raw_data: Tag) -> Course:
    print(type(raw_data))
    title = raw_data.select_one(".typography_landingH3__vTjok")
    if "Вечірній" in title.text:
        course_type = CourseType.PART_TIME
        name = "".join(title.text.split()[1:-1])
    else:
        course_type = CourseType.FULL_TIME
        name = title.text.split(" ", 1)[1]
    print(name)
    short_description = raw_data.select_one(
        ".CourseCard_courseDescription__Unsqj"
    )

    return Course(
        name=name, short_description=short_description, course_type=course_type
    )


def get_all_courses() -> list[Course]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="path/to/chromedriver", options=chrome_options
    )

    driver.get(HOME_URL)

    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [get_course_detail(course) for course in courses]


get_all_courses()
