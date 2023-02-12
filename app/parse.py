import time
import requests

from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin
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
    count_modules: int
    count_topics: int
    count_duration: str


def parse_single_course(
        course_soup: BeautifulSoup,
        course_detail_soup: BeautifulSoup
) -> Course:
    return Course(
        name=course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text.split()[1],
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=CourseType.PART_TIME if course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text.split()[-1] == "Вечірній" else CourseType.FULL_TIME,
        count_modules=int(course_detail_soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP > "
            ".typography_landingP2__KdC5Q"
        ).text.split()[0]),
        count_topics=int(course_detail_soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR > "
            ".typography_landingP2__KdC5Q"
        ).text.split()[0]),
        count_duration="Not indicated" if len(course_detail_soup) == 2 else
        course_detail_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H > "
            ".typography_landingP2__KdC5Q"
        ).text.split()[0],
    )


def get_courses_detail(course_soup: BeautifulSoup) -> list[BeautifulSoup]:
    link_course = urljoin(BASE_URL, course_soup.select_one("a")["href"])
    page = requests.get(link_course).content
    page_soup = BeautifulSoup(page, "html.parser")
    return page_soup.select(".CourseModulesHeading_headingGrid__50qAP")


def get_courses() -> list[BeautifulSoup]:
    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")
    return page_soup.select(".CourseCard_cardContainer__7_4lK")


def get_all_courses() -> list[Course]:
    courses = get_courses()

    list_courses = []
    for course_soup in courses:
        courses_detail_soup = get_courses_detail(course_soup)
        for course_detail in courses_detail_soup:
            list_courses.append(
                parse_single_course(course_soup, course_detail)
            )
    return list_courses


if __name__ == "__main__":
    start = time.perf_counter()

    courses = get_all_courses()
    for course in courses:
        print(course)

    print(f"Elapsed: {time.perf_counter() - start}")
