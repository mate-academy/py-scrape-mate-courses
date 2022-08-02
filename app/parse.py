from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def parse_single_course(product_soup: BeautifulSoup, type_: str) -> Course:
    return Course(
        name=product_soup.select_one("span.typography_landingH3__vTjok").text,
        short_description=product_soup.select_one("p").text,
        type=CourseType(type_)
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    all_courses = {
        type_.value: soup.select(
            f"div[id={type_.value}] section.CourseCard_cardContainer__7_4lK"
        )
        for type_ in CourseType
    }
    courses_list = []

    for key, value in all_courses.items():
        for data in value:
            courses_list.append(parse_single_course(data, key))
    return courses_list


if __name__ == "__main__":
    print(get_all_courses())

