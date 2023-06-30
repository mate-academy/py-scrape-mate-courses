import csv
from dataclasses import dataclass, astuple, fields
from enum import Enum

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


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:
    return Course(
        name=course_soup.select_one("a.mb-16").text,
        short_description=course_soup.select_one(
            "p.typography_landingMainText__Ux18x"
        ).text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    courses = []
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_course = soup.select(
        "#full-time section.CourseCard_cardContainer__7_4lK"
    )
    part_time_course = soup.select(
        "#part-time section.CourseCard_cardContainer__7_4lK"
    )

    courses.extend(
        [parse_single_course(
            course_soup, CourseType.FULL_TIME
        ) for course_soup in full_time_course]
    )
    courses.extend(
        [parse_single_course(
            course_soup,
            CourseType.PART_TIME
        ) for course_soup in part_time_course]
    )
    return courses


def write_courses_to_csv(courses: [Course], output_csv_path: str) -> None:
    with open(output_csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


if __name__ == "__main__":
    write_courses_to_csv(get_all_courses(), "Made_Academy")
