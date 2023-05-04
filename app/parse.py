from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_modules: str
    num_topics: str
    months_duration: str


def parse_single_course(course_soup: Tag, course_type: CourseType) -> Course:
    detail_href = course_soup.select_one("a.CourseCard_button__HTQvE").get(
        "href"
    )
    detail_page = requests.get(urljoin(BASE_URL, detail_href)).content
    detail_soup = BeautifulSoup(detail_page, "html.parser")

    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            "p.CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
        num_modules=detail_soup.select_one(
            "div.CourseModulesHeading_modulesNumber__GNdFP"
        ).text,
        num_topics=detail_soup.select_one(
            "div.CourseModulesHeading_topicsNumber__PXMnR"
        ).text,
        months_duration=detail_soup.select_one(
            "div.CourseModulesHeading_courseDuration__f_c3H"
        ).text,
    )


def get_courses_by_type(course_type: CourseType) -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(f"#{course_type.value} section")

    return [
        parse_single_course(course_soup, course_type)
        for course_soup in courses_soup
    ]


def get_all_courses() -> list[Course]:
    return [
        *get_courses_by_type(CourseType.FULL_TIME),
        *get_courses_by_type(CourseType.PART_TIME),
    ]


if __name__ == "__main__":
    print(get_all_courses())
