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
    course_type: CourseType
    modules_count: int
    topics_count: int
    duration: str


def get_course_data(url: str) -> dict:
    course_url = urljoin(BASE_URL, url)
    course_page = requests.get(course_url).content
    course_soup = BeautifulSoup(course_page, "html.parser")

    return {
        "modules_count": int(
            course_soup.select_one(
                ".CourseModulesHeading_modulesNumber__GNdFP > p"
            ).text.split()[0]
        ),
        "topics_count": int(
            course_soup.select_one(
                ".CourseModulesHeading_topicsNumber__PXMnR > p"
            ).text.split()[0]
        ),
        "duration": course_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H > p"
        ).text
    }


def parse_single_part_time_course(soup: BeautifulSoup) -> Course:
    part_time_url = soup.select_one(
        "div > a.Button_secondary__DNIuD"
    )["href"]

    return Course(
        name=soup.select_one(".ProfessionCard_title__Zq5ZY.mb-12").text,
        short_description=soup.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        course_type=CourseType.PART_TIME,
        **get_course_data(part_time_url)
    )


def parse_single_full_time_course(soup: BeautifulSoup) -> Course:
    full_time_url = soup.select_one(
        ".ProfessionCard_buttons__a0o60 > a.Button_primary__7fH0C"
    )["href"]

    return Course(
        name=soup.select_one(".ProfessionCard_title__Zq5ZY.mb-12").text,
        short_description=soup.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        course_type=CourseType.FULL_TIME,
        **get_course_data(full_time_url)
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_data = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []

    for course_data in courses_data:
        try:
            all_courses.append(parse_single_part_time_course(course_data))
        except TypeError:
            continue
        finally:
            all_courses.append(parse_single_full_time_course(course_data))
    return all_courses
