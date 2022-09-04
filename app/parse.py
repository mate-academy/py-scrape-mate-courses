from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup


HOME_URL = "https://mate.academy/ru"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def parse_single_course(courses_soup: BeautifulSoup) -> Course:
    name = courses_soup.select_one(".typography_landingH3__vTjok").text
    short_description = courses_soup.select_one(".CourseCard_courseDescription__Unsqj").text
    course_type = ("part-time" if name.split()[-1] == "Вечерний" else "full-time")
    return Course(name, short_description, course_type)


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_single_course(courses_soup) for courses_soup in courses]


def main():
    print(get_all_courses())


if __name__ == '__main__':
    main()
