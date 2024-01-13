from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

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
    duration_in_months: int


def parse_additional_info(course_link: str) -> tuple:
    page = requests.get(urljoin(BASE_URL, f"{course_link}")).content
    soup = BeautifulSoup(page, "html.parser")

    modules, topics, duration = [
        int(additional_info.text.split()[0])
        for additional_info in soup.select(
            "div.CourseModulesHeading_headingGrid__50qAP p"
        )
    ]
    return modules, topics, duration


def parse_course(course_soup: Tag) -> list[Course]:
    courses = []

    course_link_list = [
        link["href"] for link in course_soup.select("[data-qa]")
    ]

    course_type_list = [
        course_type.text for course_type in course_soup.select("a span")
    ]

    for course_type, course_link in zip(course_type_list, course_link_list):

        modules, topics, duration = parse_additional_info(course_link)

        if course_type == "Власний темп":
            courses.append(
                Course(
                    name=course_soup.select_one("a > h3").text,
                    short_description=course_soup.select_one(
                        "p:nth-child(3)"
                    ).text,
                    course_type=CourseType.PART_TIME,
                    modules_count=modules,
                    topics_count=topics,
                    duration_in_months=duration,
                )
            )

        if course_type == "Повний день":
            courses.append(
                Course(
                    name=course_soup.select_one("a > h3").text,
                    short_description=course_soup.select_one(
                        "p:nth-child(3)"
                    ).text,
                    course_type=CourseType.FULL_TIME,
                    modules_count=modules,
                    topics_count=topics,
                    duration_in_months=duration,
                )
            )
    return courses


def get_all_courses() -> list[Course]:
    all_courses = []
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    [all_courses.extend(parse_course(course_soup)) for course_soup in courses]

    return all_courses


if __name__ == "__main__":
    get_all_courses()
