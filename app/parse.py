from bs4 import BeautifulSoup
from selenium import webdriver

from dataclasses import dataclass
from enum import Enum


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:
    return Course(
        name=course_soup.select_one("a", {"class": "mb-16"}).text,
        short_description=(
            course_soup.select_one(
                "p", {"class": "typography_"}, partial=True).text
        ),
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    driver = webdriver.Chrome()
    driver.get(URL)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    courses_list = []

    for course_type in CourseType:
        section = soup.find("div", {"id": course_type.value})
        courses = section.findAll(
            "section", {"class": "CourseCard_cardContainer__7_4lK"}
        )

        for course in courses:
            courses_list.append(parse_single_course(course, course_type))

    return courses_list


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
