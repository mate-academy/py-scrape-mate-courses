import urllib.parse

import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup


MATE_ACADEMY_URL = "https://mate.academy"


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
    duration: str


def parse_course_detailed_page(url: str) -> dict:
    detailed_page = requests.get(url).content
    detailed_page_soup = BeautifulSoup(detailed_page, "html.parser")

    modules = int(detailed_page_soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text.split()[0])
    topics = int(detailed_page_soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text.split()[0])
    try:
        duration = detailed_page_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H"
        ).text
    except AttributeError:
        duration = "No info"

    return {
        "modules": modules,
        "topics": topics,
        "duration": duration
    }


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:
    detailed_page_url = urllib.parse.urljoin(
        MATE_ACADEMY_URL, course_soup.select_one("div > a")["href"]
    )
    detailed_page_data = parse_course_detailed_page(detailed_page_url)

    return Course(
        name=course_soup.select_one("a > span").text,
        short_description=course_soup.select_one("div > p").text,
        course_type=course_type,
        modules=detailed_page_data["modules"],
        topics=detailed_page_data["topics"],
        duration=detailed_page_data["duration"]
    )


def parse_courses(
        courses_soup: BeautifulSoup,
        course_type: CourseType
) -> [Course]:
    return [
        parse_single_course(course, course_type) for course in courses_soup
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_ACADEMY_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_section = soup.select("#full-time > div > section")
    part_time_section = soup.select("#part-time > div > section")

    full_time_courses = parse_courses(full_time_section, CourseType.FULL_TIME)
    part_time_courses = parse_courses(part_time_section, CourseType.PART_TIME)

    return full_time_courses + part_time_courses


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
