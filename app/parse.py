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
    type: CourseType
    modules: int
    topics: int
    duration: int


class LanguageError(Exception):
    def __init__(self):
        super().__init__('Looks like this site violates Part 6 of Article 27 '
                         'of the Law of Ukraine "On Ensuring the Functioning '
                         'of the Ukrainian Language as the State Language"')


def get_course_details(course_item, course_type: CourseType):
    course_url = course_item.select_one("a")["href"]
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

    return Course(
        name=course_item.select_one("span.typography_landingH3__vTjok")
        .text.removeprefix("Курс ").removesuffix(" Вечірній"),
        short_description=course_item.select_one("p").text,
        type=course_type, modules=modules, topics=topics,
        duration=duration)


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    if soup.select_one("html")["lang"] != "uk":
        raise LanguageError

    result = []
    for course_type in CourseType:
        course_block = soup.select_one(f"#{course_type.value}")
        courses = course_block.select(
            "section.CourseCard_cardContainer__7_4lK"
        )
        for course_item in courses:
            result.append(get_course_details(course_item, course_type))
            print(".", end="")
    print("")

    return result


if __name__ == '__main__':
    for course in get_all_courses():
        print(course)
