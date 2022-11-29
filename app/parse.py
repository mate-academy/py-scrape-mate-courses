from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

URL = "https://mate.academy"


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


def parse_detail_page(url: str, course_type: CourseType) -> tuple:
    response = requests.get(URL + url)
    soup = BeautifulSoup(response.content, "html.parser")

    modules = soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text

    topics = soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text

    duration = None

    if course_type == CourseType.FULL_TIME:
        duration = soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H"
        ).text

    return modules, topics, duration


def get_single_info(soup: BeautifulSoup) -> Course:
    href = soup.find("a", class_="mb-16").get("href")
    name = soup.find("span", class_="typography_landingH3__vTjok").text
    description = soup.find(
        "p", class_="CourseCard_courseDescription__Unsqj"
    ).text
    course_type = (
        CourseType.PART_TIME
        if name.split()[-1] == "Вечірній"
        else CourseType.FULL_TIME
    )

    modules, topics, duration = parse_detail_page(href, course_type)

    print(name, course_type, duration, topics, duration)

    return Course(
        name=name,
        short_description=description,
        course_type=course_type,
        modules=modules,
        topics=topics,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    courses = soup.find_all(
        "section", class_="CourseCard_cardContainer__7_4lK"
    )

    return [get_single_info(course) for course in courses]


if __name__ == "__main__":
    get_all_courses()
