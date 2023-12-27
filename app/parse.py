import csv
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, element

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def _create_course_instance(name: str,
                            short_description: str,
                            course_type: str) -> Course:
    if course_type == "Власний темп":
        course_type = CourseType.FULL_TIME
    if course_type == "Повний день":
        course_type = CourseType.PART_TIME
    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type,
    )


def _parse_single_course(course: element.Tag) -> list[Course]:
    name = course.select_one("a.ProfessionCard_title__Zq5ZY").text
    short_description = course.select(
        "p.typography_landingTextMain__Rc8BD"
    )[1].text
    course_types = [
        course.text
        for course
        in course.select("div.ProfessionCard_buttons__a0o60 > a > span")
    ]
    return [_create_course_instance(
        name=name,
        short_description=short_description,
        course_type=course_type
    ) for course_type in course_types]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select("div.ProfessionsListSection_cardsWrapper___Zpyd > "
                          "div.ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course in courses:
        all_courses.extend(_parse_single_course(course))
    return all_courses


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    with open(output_csv_path, "w", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Name", "Short Description", "Course Type"])
        for course in courses:
            csv_writer.writerow(
                [course.name, course.short_description, course.course_type]
            )


if __name__ == "__main__":
    main("courses.csv")
