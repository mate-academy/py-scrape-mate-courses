from dataclasses import dataclass, fields
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/en/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


PRODUCT_FIELDS = [field.name for field in fields(Course)]


def course_type_(product_soup: BeautifulSoup) -> CourseType:
    name = product_soup.select_one(".typography_landingH3__vTjok").text
    if "Flex" in name:
        return CourseType.PART_TIME

    return CourseType.FULL_TIME


def parse_single_course(product_soup: BeautifulSoup) -> Course:
    return Course(
        name=product_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=product_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type_(product_soup),
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    products = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_single_course(product_soup) for product_soup in products]
