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
    modules: int
    topics: int
    duration: str


def pars_single_course(course_soup: Tag) -> Course:
    detail_course_url = urljoin(
        BASE_URL,
        course_soup.select_one("a.mb-16")["href"]
    )
    detail_course_page = requests.get(detail_course_url).content
    detail_course_soup = BeautifulSoup(detail_course_page, "html.parser")

    course_name = course_soup.select_one(
        ".typography_landingH3__vTjok"
    ).text
    course_description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    number_modules = int(detail_course_soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text.split()[0])
    number_topics = int(detail_course_soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text.split()[0])
    course_duration = detail_course_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H > p"
    )

    if course_duration:
        course_duration = course_duration.text
    else:
        course_duration = "At your discretion"

    return Course(
        name=course_name,
        short_description=course_description,

        course_type=CourseType.PART_TIME.value
        if course_name.split()[-1] == "Вечірній"
        else CourseType.FULL_TIME.value,

        modules=number_modules,
        topics=number_topics,
        duration=course_duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [pars_single_course(course_soup) for course_soup in courses]


if __name__ == "__main__":
    get_all_courses()
