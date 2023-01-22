from dataclasses import dataclass
from enum import Enum

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


def pars_single_curse(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one("span.typography_landingH3__vTjok").text
    short_description = course_soup.select_one("p.typography_landingP1__N9PXd").text
    course_type = CourseType.PART_TIME if name.split()[-1] == "Вечерний" else CourseType.FULL_TIME
    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    page = requests.get("https://mate.academy/ru").content
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(".CourseCard_cardContainer__7_4lK")
    return [pars_single_curse(course_soup) for course_soup in courses_soup]


def main():
    print(get_all_courses())


if __name__ == '__main__':
    main()
