import csv
from dataclasses import dataclass, fields, astuple
from enum import Enum
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


QUOTE_FIELDS = [field.name for field in fields(Course)]


def check_course_type(course_card: Tag) -> list[CourseType]:
    course_types = course_card.select(
        ".ProfessionCard_buttons__a0o60 > a[data-qa]"
    )
    return [
        CourseType.FULL_TIME if "fulltime" in course_type["data-qa"]
        else CourseType.PART_TIME
        for course_type in course_types
    ]


def parse_single_course(course: Tag) -> [Course]:
    return ([Course(
        name=course.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        course_type=course_type
    )
        for course_type in check_course_type(course)
    ])


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courser = []
    for course_soup in courses:
        all_courser.extend(parse_single_course(course_soup))
    return all_courser


def write_courses_to_csv(courses: [Course], path: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(QUOTE_FIELDS)
        writer.writerows(astuple(course) for course in courses)


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    write_courses_to_csv(courses=courses, path=output_csv_path)


if __name__ == "__main__":
    main("quotes.csv")
