from urllib.parse import urljoin

import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    modules: int
    topics: int
    duration: int


def get_detail_course_info(course, course_type):
    course_url = course.select_one("a")["href"]
    page = requests.get(urljoin(BASE_URL, course_url)).content
    soup = BeautifulSoup(page, "html.parser")

    modules = int(soup.select_one(
        "div.CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text.split()[0])
    topics = int(soup.select_one(
        "div.CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text.split()[0])
    if course_type == CourseType.FULL_TIME:
        duration = int(soup.select_one(
            "div.CourseModulesHeading_courseDuration__f_c3H > p"
        ).text.split()[0])
    else:
        duration = None

    return (modules, topics, duration)


def get_single_course(course, course_type: CourseType):
    modules, topics, duration = get_detail_course_info(course, course_type)

    return Course(
        name=course.select_one("span.typography_landingH3__vTjok")
        .text.replace("Курс ", "")
        .replace(" Вечірній", ""),
        short_description=course.select_one("p").text,
        type=course_type,
        modules=modules,
        topics=topics,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    result = []
    for course_type in CourseType:
        course_block = soup.select_one(f"#{course_type.value}")
        courses = course_block.select(
            "section.CourseCard_cardContainer__7_4lK"
        )
        for course in courses:
            result.append(get_single_course(course, course_type))

    return result


def main():
    get_all_courses()


if __name__ == '__main__':
    main()
