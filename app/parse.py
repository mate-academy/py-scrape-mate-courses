from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, Tag
from selenium import webdriver


COURSES_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_one_course(item: Tag) -> Course:
    name = item.select_one(".typography_landingH3__vTjok").text
    course_type = (CourseType.PART_TIME
                   if "Вечірній" in name
                   else CourseType.FULL_TIME)
    return Course(
        name=name,
        short_description=item.select_one(
            ".typography_landingMainText__Ux18x"
        ).text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(60)

    driver.get(COURSES_URL)
    source = BeautifulSoup(driver.page_source, "html.parser")
    courses = source.select(".CourseCard_cardContainer__7_4lK")
    driver.close()

    return [parse_one_course(course) for course in courses]


for element in get_all_courses():
    print(element)
