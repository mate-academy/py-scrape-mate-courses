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
    modules: str
    topics: str
    duration: str


def parse_detail_page(course_url: str, course_type: CourseType) -> tuple:
    res = requests.get(BASE_URL + course_url)
    soup = BeautifulSoup(res.content, "html.parser")

    modules = soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text.split()[0]

    topics = soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text.split()[0]

    if course_type == CourseType.FULL_TIME:
        duration = soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H p"
        ).get_text()
    else:
        duration = "All the time you need"

    return modules, topics, duration


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one("span.typography_landingH3__vTjok").text
    description = course_soup.select_one(
        "p.CourseCard_courseDescription__Unsqj"
    ).text

    course_url = course_soup.find("a", class_="mb-16").get("href")

    course_type = (
        CourseType.PART_TIME if "вечірній" in name.lower()
        else CourseType.FULL_TIME
    )

    modules, topics, duration = parse_detail_page(course_url, course_type)

    return Course(
        name=name,
        short_description=description,
        course_type=course_type,
        modules=modules,
        topics=topics,
        duration=duration,

    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


if __name__ == "__main__":
    print(get_all_courses())
