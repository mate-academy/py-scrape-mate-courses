import csv
from dataclasses import dataclass
from enum import Enum
from typing import Optional

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


def check_full_time(
        name: str,
        short_description: str,
        course_soup: BeautifulSoup
) -> Course | None:
    element = course_soup.find(
        "a",
        {"data-qa": "fulltime-course-more-details-button"}
    )

    if element:
        full_time = Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.FULL_TIME
        )
        return full_time


def check_part_time(
        name: str,
        short_description: str,
        course_soup: BeautifulSoup
) -> Course | None:
    element = course_soup.find(
        "a",
        {"data-qa": "parttime-course-more-details-button"}
    )

    if element:
        part_time = Course(
            name=name,
            short_description=short_description,
            course_type=CourseType.PART_TIME
        )
        return part_time


def parse_single_course_page(
        course_soup: BeautifulSoup
) -> tuple[Optional[Course], Optional[Course]]:
    name = course_soup.find(
        "h3",
        class_="typography_landingH3__vTjok ProfessionCard_title__Zq5ZY mb-12"
    ).text
    short_description = course_soup.find(
        "p",
        class_="typography_landingTextMain__Rc8BD mb-32"
    ).text

    part_time = check_part_time(
        name=name,
        short_description=short_description,
        course_soup=course_soup
    )
    full_time = check_full_time(
        name=name,
        short_description=short_description,
        course_soup=course_soup
    )

    return part_time, full_time


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [
        course
        for course_type in courses
        for course in parse_single_course_page(course_type)
        if course
    ]


def write_courses_to_csv(courses: list[Course], output_csv_path: str) -> None:
    with open(output_csv_path, "w", newline="", encoding="utf-8") as file:
        written = csv.writer(file)
        written.writerow(["name", "short_description", "course_type"])
        for course in courses:
            written.writerow(
                [course.name, course.short_description, course.course_type]
            )


def main(output_csv_path: str) -> None:
    course = get_all_courses()
    write_courses_to_csv(course, output_csv_path)


if __name__ == "__main__":
    main("courses.csv")
