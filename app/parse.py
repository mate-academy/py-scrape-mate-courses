from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    count_modules: str
    count_topics: str
    duration: str


def parse_detail_of_course(full_course_name: str) -> list:
    full_course_name = full_course_name.lower().split()
    course_name = full_course_name[1].replace("/", "-")
    if full_course_name[-1] == "вечірній":
        course_name = f"{course_name}-parttime"

    course_url = urljoin(HOME_URL, f"courses/{course_name}")
    page = requests.get(course_url).content
    soup = BeautifulSoup(page, "html.parser")

    css_selector = ".CourseModulesHeading_headingGrid__50qAP > div > p"
    course_modules_heading = soup.select(css_selector)

    count_modules = course_modules_heading[0].text
    count_topics = course_modules_heading[1].text
    duration = (
        course_modules_heading[2].text
        if len(course_modules_heading) > 2
        else "no information available"
    )

    return [count_modules, count_topics, duration]


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".CourseCard_flexContainer__dJk4p"
    ).text.replace("Детальніше", "")
    course_type = (
        CourseType("part-time")
        if name.split()[-1] == "Вечірній"
        else CourseType("full-time")
    )

    detail_of_course = parse_detail_of_course(full_course_name=name)

    return Course(
        name=name,
        short_description=short_description,
        type=course_type,
        count_modules=detail_of_course[0],
        count_topics=detail_of_course[1],
        duration=detail_of_course[-1],
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in tqdm(courses)]


if __name__ == "__main__":
    get_all_courses()
