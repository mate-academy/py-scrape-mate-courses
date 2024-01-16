import csv

from dataclasses import dataclass, astuple, fields
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

HOME_URL = "https://mate.academy/"

COURSES_CSV_PATH = "courses.csv"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    topics: int
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def get_additional_info(url: str) -> (int, int, str):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")

    modules = int(soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP"
    ).text.split()[0])
    topics = int(soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR"
    ).text.split()[0])
    duration = soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H"
    ).text

    return modules, topics, duration


def parse_single_course(course_soup: Tag) -> [Course]:
    buttons = course_soup.select_one(".ProfessionCard_buttons__a0o60")
    types = buttons.select("span")
    links = buttons.select("a")

    course_info = []

    for i, type_ in enumerate(types):
        course_type = None

        if type_.text == "Власний темп":
            course_type = CourseType.PART_TIME
        elif type_.text == "Повний день":
            course_type = CourseType.FULL_TIME

        url_detail_info = urljoin(HOME_URL, links[i]["href"])
        modules, topics, duration = get_additional_info(url_detail_info)
        course_info.append((course_type, modules, topics, duration))

    course = [
        Course(
            name=course_soup.select_one("h3").text,
            short_description=course_soup.select("p")[-1].text,
            course_type=info[0],
            modules=info[1],
            topics=info[2],
            duration=info[3]

        ) for info in course_info
    ]

    return course


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    courses = []

    for course_soup in courses_soup:
        courses.extend(parse_single_course(course_soup))

    return courses


def write_to_csv(courses: [Course], csv_path: str) -> None:
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main() -> None:
    courses = get_all_courses()
    write_to_csv(courses, COURSES_CSV_PATH)


if __name__ == "__main__":
    main()
