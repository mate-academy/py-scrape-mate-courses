from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

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
    course_type: CourseType
    modules: int
    topics: int
    duration: int


def home_soup(course_soup: BeautifulSoup) -> list:
    url = course_soup.select_one(".mb-16")["href"]
    course_type_eval = course_soup.select_one(".mb-16")["rel"]
    page = requests.get(urljoin(BASE_URL, url)).content
    soup_optional = BeautifulSoup(page, "html.parser")
    modules = int(soup_optional.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text.split()[0])
    topics = int(soup_optional.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text.split()[0])

    if course_type_eval:
        course_type = CourseType.PART_TIME
    else:
        course_type = CourseType.FULL_TIME

    try:
        duration = soup_optional.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H"
        ).text.split()[0][0]
    except AttributeError:
        duration = 0

    return [course_type, modules, topics, int(duration)]


def parse_single_course(course_soup: BeautifulSoup) -> [Course]:
    home = home_soup(course_soup)

    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=home[0],
        modules=home[1],
        topics=home[2],
        duration=home[3],
    )


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
