from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver

URL = "https://mate.academy/"


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
    duration: int = None


def get_additional_info(course_url: str) -> dict:
    course_page = requests.get(course_url).content
    soup = BeautifulSoup(course_page, "html.parser")

    modules = int(soup.select_one(
        "div.CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text.split()[0])
    topics = int(soup.select_one(
        "div.CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text.split()[0])
    duration_soup = soup.select_one(
        "div.CourseModulesHeading_courseDuration__f_c3H > p"
    )

    if duration_soup:
        duration = int(duration_soup.text.split()[0][-1])
    else:
        duration = None

    return dict(
        modules=modules,
        topics=topics,
        duration=duration
    )


def parse_one_course(course_soup: Tag, course_type: CourseType) -> Course:
    name = course_soup.select_one("a > span.typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        "p.CourseCard_courseDescription__Unsqj"
    ).text
    course_url = URL + course_soup.select_one("a.mb-16")["href"]

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type,
        **get_additional_info(course_url)
    )


def get_all_courses() -> list[Course]:
    with webdriver.Chrome() as driver:
        driver.get(URL)
        page = driver.page_source

    soup = BeautifulSoup(page, "html.parser")

    full_time_courses = soup.select("div#full-time section")
    part_time_courses = soup.select("div#part-time section")

    all_courses = []

    for course in full_time_courses:
        all_courses.append(parse_one_course(
            course, course_type=CourseType.FULL_TIME
        ))

    for course in part_time_courses:
        all_courses.append(parse_one_course(
            course, course_type=CourseType.PART_TIME
        ))

    return all_courses
