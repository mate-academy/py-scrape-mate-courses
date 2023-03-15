import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_modules: Optional[int] = None
    num_topics: Optional[int] = None
    num_duration: Optional[int] = None


def extract_course_details(course_soup: BeautifulSoup) -> tuple[str, str]:

    name = course_soup.select_one(".typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        ".typography_landingP1__N9PXd"
    ).text

    return name, short_description


def parse_single_course(course_soup: BeautifulSoup) -> Course:

    name, short_description = extract_course_details(course_soup)
    link = "https://mate.academy/" + course_soup.select_one(
        ".Button_large__rIMVg"
    )["href"]
    course_page = requests.get(link).content
    course_soup = BeautifulSoup(course_page, "html.parser")

    # Extract the number of modules, topics and duration from the course code
    module_code_element = course_soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text
    num_modules = int(re.search(r"\d+", module_code_element).group())

    topic_code_element = course_soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text
    num_topics = int(re.search(r"\d+", topic_code_element).group())

    duration_code_element = course_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H"
    )
    num_duration = int(
        re.search(r"\d+", duration_code_element.text).group()
    ) if duration_code_element else None

    return Course(
        name=name,
        short_description=short_description,
        course_type=CourseType.PART_TIME
        if "Вечірній" in name else CourseType.FULL_TIME,
        num_modules=num_modules,
        num_topics=num_topics,
        num_duration=num_duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get("https://mate.academy/").content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


def main() -> None:
    courses = get_all_courses()
    for course in courses:
        print(course.name,
              course.short_description,
              course.course_type.value,
              course.num_modules,
              course.num_topics,
              course.num_duration)


if __name__ == "__main__":
    main()
