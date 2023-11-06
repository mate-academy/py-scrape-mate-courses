import csv
from dataclasses import dataclass
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
    course_type: list[CourseType] | CourseType


def parse_single_course_page(course_soup: BeautifulSoup) -> Course:
    name = course_soup.find(
        "h3",
        class_="typography_landingH3__vTjok ProfessionCard_title__Zq5ZY mb-12"
    ).text.split(" ")[0]
    short_description = course_soup.find(
        "p", class_="typography_landingTextMain__Rc8BD mb-32"
    ).text
    course_type_elements = course_soup.find_all(
        "span", class_="ButtonBody_buttonText__FMZEg"
    )
    course_type_texts = [c.text for c in course_type_elements]

    course_types = []
    for course_type_text in course_type_texts:
        if course_type_text == "Власний темп":
            course_types.append(CourseType.PART_TIME)
        elif course_type_text == "Повний день":
            course_types.append(CourseType.FULL_TIME)

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_types,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course_page(course) for course in courses]


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
