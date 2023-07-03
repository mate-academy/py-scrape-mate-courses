from __future__ import annotations

import csv
from dataclasses import dataclass, astuple, fields
from enum import Enum
import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType

    def get_single_course(
            self,
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

    def get_all_courses(self) -> list[Course]:
        courses = []
        page = requests.get(BASE_URL).content
        soup = BeautifulSoup(page, "html.parser")

        course_types = [
            (
                "#full-time section.CourseCard_cardContainer__7_4lK",
                CourseType.FULL_TIME
            ),
            (
                "#part-time section.CourseCard_cardContainer__7_4lK",
                CourseType.PART_TIME
            )
        ]

        for course_selector, course_type in course_types:
            courses.extend([
                self.get_single_course(self, course_soup, course_type)
                for course_soup in soup.select(course_selector)
            ])
        return courses


COURSE_FIELDS = [field.name for field in fields(Course)]


def write_to_csv(courses: list[Course], output_csv_path: str) -> None:
    with open(output_csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


if __name__ == "__main__":
    write_to_csv(Course.get_all_courses(Course), "Made_Academy.csv")
