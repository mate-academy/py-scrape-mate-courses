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
    modules: str
    topics: str
    duration_months: str


def get_single_course(course_card: Tag, crs: str) -> Course:
    url_course = urljoin(BASE_URL, course_card.select_one("a")["href"])
    url_course_detail = urljoin(url_course, "#course-program")
    resp = requests.get(url_course_detail).content
    soup = BeautifulSoup(resp, "html.parser")
    if soup.select_one(".CourseModulesHeading_courseDuration__f_c3H"):
        duration = soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H").text.split()[0]
    else:
        duration = ""
    course = Course(
        name=course_card.select_one("span.typography_landingH3__vTjok").text,
        short_description=course_card.select_one(
            "p.CourseCard_courseDescription__Unsqj").text,
        course_type=CourseType(crs),
        modules=soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP").text.split()[0],
        topics=soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR").text.split()[0],
        duration_months=duration
    )
    return course


def get_all_courses() -> list[Course]:
    resp = requests.get(BASE_URL).content
    soup = BeautifulSoup(resp, "html.parser")
    part_blocks = soup.select("#full-time,#part-time")
    all_courses = list()
    for block in part_blocks:
        course_cards = block.select("section.CourseCard_cardContainer__7_4lK")
        all_courses.extend([
            get_single_course(course_card, block["id"]) for course_card in course_cards
        ])
    return all_courses


def main():
    for course in get_all_courses():
        print(course)


if __name__ == "__main__":
    main()