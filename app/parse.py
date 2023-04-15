from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

from bs4 import BeautifulSoup, element
import requests

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_modules: int
    num_topics: int
    duration: str | None


def parse_additional_info(link: str) -> tuple:
    additional_info_url = urljoin(BASE_URL, link)
    page = requests.get(additional_info_url).content
    soup = BeautifulSoup(page, "html.parser")

    num_modules = int(soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text.split()[0])
    num_topics = int(soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text.split()[0])
    duration_field = soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H > p"
    )
    duration = (
        duration_field.text.replace("місяців", "months")
        if duration_field is not None
        else None
    )

    return num_modules, num_topics, duration


def parse_single_course(course_soup: element.Tag) -> Course:
    name = course_soup.select_one("span").text
    link = course_soup.select_one("a")["href"]
    num_modules, num_topics, duration = parse_additional_info(link)

    return Course(
        name=name,
        short_description=course_soup.select_one("p").text,
        course_type=(
            CourseType.PART_TIME if "Вечірній" in name
            else CourseType.FULL_TIME
        ),
        num_modules=num_modules,
        num_topics=num_topics,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in courses]
