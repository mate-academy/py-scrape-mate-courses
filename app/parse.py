from dataclasses import dataclass
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType

    def __str__(self):
        return f"name={self.name};" \
               f" short_description={self.short_description};" \
               f" course_type={self.course_type.value}"


def parse_single_product(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(".typography_landingMainText__Ux18x.CourseCard_courseDescription__Unsqj").text
    course_type = CourseType.PART_TIME if "Вечірній" in name else CourseType.FULL_TIME

    return Course(name=name, short_description=short_description, course_type=course_type)


def get_all_courses() -> List[Course]:
    page = requests.get("https://mate.academy").content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    parsed_courses = [parse_single_product(course_soup) for course_soup in courses]

    return parsed_courses


if __name__ == "__main__":
    all_courses = get_all_courses()
    for course in all_courses:
        print(course)
