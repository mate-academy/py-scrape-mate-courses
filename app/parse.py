from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
from pprint import pprint

import requests

PARSE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def study_format(course_soup: BeautifulSoup) -> bool:
    value = course_soup.select_one(
        ".typography_landingH3__vTjok"
    ).text.split()[-1]

    return value == "Вечірній"


def parse_simple_cource(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=CourseType.PART_TIME.value if study_format(
            course_soup) else CourseType.FULL_TIME.value
    )


def get_all_courses() -> list[Course]:
    page = requests.get(PARSE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    course_soup = soup.select(".CourseCard_cardContainer__7_4lK")
    print(course_soup)

    res = [parse_simple_cource(course) for course in course_soup]
    pprint(res)
    return res

# TODO: I DON'T understund how ti do this task without selenium, hardcode-json_load and without any links in networks.
