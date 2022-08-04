from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


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
    duration: int = None


def parse_course_info(course_soup, course_type):
    course_url = course_soup.select_one("a")["href"]
    page = requests.get(urljoin(BASE_URL, course_url)).content
    soup = BeautifulSoup(page, "html.parser")

    modules = int(soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP > p").text.split()[0])
    topics = int(soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR > p").text.split()[0])
    if course_type == CourseType.FULL_TIME:
        duration = int(soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H > p").text.split()[0])
    else:
        duration = None

    return {
        "modules": modules,
        "topics": topics,
        "duration": duration
    }


def parse_single_course(course_soup, course_type) -> Course:
    course_info_data = parse_course_info(course_soup, course_type)

    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj").text,
        type=course_type,
        modules=course_info_data["modules"],
        topics=course_info_data["topics"],
        duration=course_info_data["duration"]
    )


def full_time_courses(full_time_soup) -> list[Course]:
    return [
        parse_single_course(course_soup, CourseType.FULL_TIME)
        for course_soup in full_time_soup
    ]


def part_time_courses(part_time_soup) -> list[Course]:
    return [
        parse_single_course(course_soup, CourseType.PART_TIME)
        for course_soup in part_time_soup
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_soup = soup.select("#full-time .CourseCard_cardContainer__7_4lK")

    part_time_soup = soup.select("#part-time .CourseCard_cardContainer__7_4lK")

    all_courses = full_time_courses(
        full_time_soup) + part_time_courses(part_time_soup)

    return all_courses


def main():
    get_all_courses()


if __name__ == "__main__":
    main()
