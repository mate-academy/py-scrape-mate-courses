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
    modules: str
    topics: str
    duration: str


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one("span.typography_landingH3__vTjok").text,
    short_description = course_soup.select_one("p.CourseCard_courseDescription__Unsqj").text,
    course_type = (CourseType.PART_TIME if name[0].split()[-1] == "Вечірній" else CourseType.FULL_TIME)

    full_info_url = urljoin(BASE_URL, course_soup.select_one("a.mb-16")["href"])
    detail_page = requests.get(full_info_url).content
    detail_soup = BeautifulSoup(detail_page, "html.parser")

    modules = detail_soup.select_one(".CourseModulesHeading_modulesNumber__GNdFP").text
    topics = detail_soup.select_one(".CourseModulesHeading_topicsNumber__PXMnR").text
    duration = detail_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H"
    ).text if detail_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H"
    ) else "Sorry, we don't know how long you will study"

    return Course(
        name=name[0],
        short_description=short_description[0],
        course_type=course_type,
        modules=modules,
        topics=topics,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    course = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in course]


def main():
    print(get_all_courses())


if __name__ == "__main__":
    main()
