import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin


BASE_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    topics: int
    duration: str


def get_course_additional_details(course_detail_url: str) -> dict:
    page = requests.get(urljoin(BASE_URL, course_detail_url)).content
    course_detail_page_soup = BeautifulSoup(page, "html.parser")

    course_additional_details = dict(
        modules=int(course_detail_page_soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP"
        ).text.split()[0]),
        topics=int(course_detail_page_soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR"
        ).text.split()[0]),
        duration=course_detail_page_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H"
        ).text,
    )

    return course_additional_details


def get_single_course_full_details(course: BeautifulSoup) -> Course:
    course_detail_url = course.select_one(".mb-16")["href"]
    course_type_in_url = course.select_one("a.mb-16")["href"].split("-")[-1]

    course_base_details = dict(
        name=course.select_one(".typography_landingH3__vTjok").text,
        short_description=course.select_one(
            "p.CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=(
            CourseType.PART_TIME
            if course_type_in_url == "parttime"
            else CourseType.FULL_TIME
        )
    )
    course_additional_details = get_course_additional_details(
        course_detail_url
    )

    return Course(
        **course_base_details,
        **course_additional_details
    )


def get_all_courses() -> list[Course]:
    page_content = requests.get(BASE_URL).content
    base_soup = BeautifulSoup(page_content, "html.parser")

    courses = base_soup.select(".CourseCard_cardContainer__7_4lK")

    return [get_single_course_full_details(course) for course in courses]
