from dataclasses import dataclass
from enum import Enum

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
    duration: str


def get_additional_info(url: str) -> tuple:
    page = requests.get(url).content
    course_soup = BeautifulSoup(page, "html.parser")

    modules = int(course_soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP p"
    ).text.split()[0])
    topics = int(course_soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR p"
    ).text.split()[0])
    duration = course_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H > p"
    )

    if duration:
        duration_count = duration.text
    else:
        duration_count = None

    return modules, topics, duration_count


def parse_courses(course_soup: BeautifulSoup) -> Course:
    if course_soup.select_one(".typography_landingH3__vTjok").text.split()[-1] == "Вечірній":
        course_type = CourseType.PART_TIME
    else:
        course_type = CourseType.FULL_TIME

    modules, topics, duration = get_additional_info(
        BASE_URL + course_soup.select_one("a")["href"]
    )

    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text.split()[1],
        short_description=course_soup.select_one("div.CourseCard_flexContainer__dJk4p > p").text,
        course_type=course_type,
        modules=modules,
        topics=topics,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_courses(course_soup) for course_soup in courses]


if __name__ == '__main__':
    print(get_all_courses())
