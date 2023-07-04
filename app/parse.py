from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, ResultSet

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: str
    topics: str
    duration: str


def get_detail_info_soup(detail_url: str) -> list[int | str]:
    page = requests.get(urljoin(BASE_URL, detail_url)).content
    page_soup = BeautifulSoup(page, "html.parser")

    modules = page_soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text
    topics = page_soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text
    duration = page_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H"
    ).text
    return [modules, topics, duration]


def get_course(soup: BeautifulSoup) -> Course:
    name = soup.select_one(
        "span.typography_landingH3__vTjok"
    ).text.replace("Курс ", "")
    detail_url = soup.select_one(".mb-16")["href"]
    info = get_detail_info_soup(detail_url=detail_url)

    course_type = (
        CourseType.PART_TIME
        if name.endswith("flex")
        else CourseType.FULL_TIME
    )

    return Course(
        name=name,
        short_description=soup.select_one(
            "p.typography_landingMainText__Ux18x."
            "CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
        modules=info[0],
        topics=info[1],
        duration=info[2],
    )


def get_courses_soups_list() -> ResultSet:
    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")

    courses = page_soup.select(".CourseCard_cardContainer__7_4lK")

    return courses


def get_all_courses() -> list[Course]:
    all_courses_soup = get_courses_soups_list()

    result = [get_course(soup) for soup in all_courses_soup]

    return result
