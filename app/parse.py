from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import bs4.element
import requests
from bs4 import BeautifulSoup

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules_count: int
    topics_count: int
    duration_months: str | None


def get_info_from_course_page(course_page_url: str) -> dict:
    course_page = requests.get(course_page_url)
    course_page_soup = BeautifulSoup(course_page.content, "html.parser")

    try:
        duration = course_page_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H"
        ).text.split(" ")[0]
    except AttributeError:
        duration = None

    return {
        "modules_count": int(
            course_page_soup.select_one(
                ".CourseModulesHeading_modulesNumber__GNdFP"
            ).text.split(" ")[0]
        ),
        "topics_count": int(
            course_page_soup.select_one(
                ".CourseModulesHeading_topicsNumber__PXMnR"
            ).text.split(" ")[0]
        ),
        "duration_months": duration,
    }


def create_course_from_course_soup(course_soup: bs4.Tag) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    course_page_url = urljoin(URL, course_soup.select_one("a")["href"])
    get_info_from_course_page(course_page_url)
    return Course(
        name=name,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=CourseType.PART_TIME
        if "Вечірній" in name
        else CourseType.FULL_TIME,
        **get_info_from_course_page(course_page_url)
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    full_time_courses = soup.select("section.CourseCard_cardContainer__7_4lK")
    return [
        create_course_from_course_soup(course) for course in full_time_courses
    ]


if __name__ == "__main__":
    print(get_all_courses())
