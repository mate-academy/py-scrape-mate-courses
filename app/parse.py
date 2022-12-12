import logging
import sys
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

MATE_URL = "https://mate.academy/"


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout),
    ]
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    modules: int
    topics: int
    duration: int
    course_type: CourseType


def get_course_info(url: str) -> tuple:
    page = requests.get(url).content
    course_soup = BeautifulSoup(page, "html.parser")

    modules = course_soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP p"
    ).text.split()[0]
    topics = course_soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR p"
    ).text.split()[0]
    duration = 0
    if "CourseModulesHeading_courseDuration__f_c3H" in course_soup:
        duration = course_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H p"
        ).text.split()[0]

    return int(modules), int(topics), int(duration)


def parse_single_course(
        course_soup: BeautifulSoup, course_type: CourseType
) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    logging.info(f'Parsing course "{name}"')

    modules, topics, duration = get_course_info(
        MATE_URL + course_soup.select_one("a")["href"]
    )

    return Course(
        name=name,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        modules=modules,
        topics=topics,
        duration=duration,
        course_type=course_type,
    )


def get_all_courses() -> [Course]:
    logging.info("Start parsing courses")
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_courses = soup.select("#full-time section")
    part_time_courses = soup.select("#part-time section")

    logging.info("Start parsing full-time courses")
    courses = [
        parse_single_course(course_soup, CourseType.FULL_TIME)
        for course_soup in full_time_courses
    ]
    logging.info("Start parsing part-time courses")
    courses.extend([
        parse_single_course(course_soup, CourseType.PART_TIME)
        for course_soup in part_time_courses
    ])
    logging.info("End parsing")

    return courses
