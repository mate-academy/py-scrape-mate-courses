from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"
HOME_URL = urljoin(BASE_URL, "en")
PAGE = requests.get(HOME_URL).content
SOUP = BeautifulSoup(PAGE, "html.parser")


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: Tag) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".typography_landingP1__N9PXd"
    ).text
    return Course(
        name=" ".join(name.split()[:-1]),
        short_description=short_description,
        course_type=(
            CourseType.PART_TIME
            if name.split()[-2] == "Flex"
            else CourseType.FULL_TIME
        )
    )


def get_all_courses() -> [Course]:
    course = SOUP.select(".CourseCard_cardContainer__7_4lK")
    return [parse_single_course(course_soup) for course_soup in course]


if __name__ == "__main__":
    get_all_courses()
