from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_of_modules: int
    num_of_topics: int
    duration: str


URL = "https://mate.academy/"


def parse_details_course(link: str) -> dict:
    url = urljoin(URL, link)
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html.parser")

    num_of_modules = soup.select_one(
        "div.CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text
    num_of_modules = int(num_of_modules.split()[0])

    num_of_topics = soup.select_one(
        "div.CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text
    num_of_topics = int(num_of_topics.split()[0])

    duration = soup.select_one(
        "div.CourseModulesHeading_courseDuration__f_c3H > p"
    )
    duration = duration.text if duration else None

    return {
        "num_of_modules": num_of_modules,
        "num_of_topics": num_of_topics,
        "duration": duration,
    }


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text

    link = course_soup.select_one(
        "div.CourseCard_flexContainer__dJk4p a[href]"
    )["href"]

    details = parse_details_course(link)
    return Course(
        name=name,
        short_description=course_soup.select_one(
            ".typography_landingMainText__Ux18x"
        ).text,
        course_type=CourseType.PART_TIME if "Вечірній" in name
        else CourseType.FULL_TIME,
        num_of_modules=details["num_of_modules"],
        num_of_topics=details["num_of_topics"],
        duration=details["duration"],
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


print(get_all_courses())
