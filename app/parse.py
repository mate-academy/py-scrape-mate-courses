import csv
from dataclasses import dataclass, fields, astuple
from enum import Enum

import requests
from bs4 import BeautifulSoup, PageElement

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


COURSE_FIELD = [field.name for field in fields(Course)]


def parse_single_course(course: PageElement) -> [Course]:
    name = course.select_one("a.typography_landingH3__vTjok").text
    short_description = course.select_one("p.mb-32").text
    course_type = course.select("div.ProfessionCard_buttons__a0o60 > a")
    all_courses = []

    for type_of_course in course_type:
        course = Course(
            name=name,
            short_description=short_description,
            course_type=(
                CourseType.PART_TIME
                if type_of_course.text == "Власний темп"
                else CourseType.FULL_TIME
            )
        )

        all_courses.append(course)

    return all_courses


def get_single_page_quote(page_soup: BeautifulSoup) -> [Course]:
    courses = (
        page_soup.select_one(".ProfessionsListSection_cardsWrapper___Zpyd")
    )

    return [
        course
        for i in range(0, len(courses) - 1)
        for course in parse_single_course(courses.contents[i])
    ]


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    all_courses = get_single_page_quote(soup)
    print(all_courses)
    return all_courses


def write_vacancies_to_csv(courses: [Course], output_csv_path: str) -> None:
    with open(output_csv_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELD)
        writer.writerows([astuple(course) for course in courses])


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    write_vacancies_to_csv(courses=courses, output_csv_path=output_csv_path)


if __name__ == "__main__":
    main("quotes.csv")
