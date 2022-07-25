import csv
import logging
import sys
from dataclasses import dataclass, fields, astuple
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"

COURSES_OUTPUT_CSV_PATH = "courses.csv"


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout)
    ],
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course_soup, course_type: CourseType) -> Course:
    return Course(
        name=course_soup.select_one(".mb-16")
        .text.replace("Курс ", "")
        .replace(" Вечірній", ""),
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        type=course_type,
    )


def get_full_time_courses(full_time_soup: BeautifulSoup) -> [Course]:
    courses = full_time_soup.select(".CourseCard_cardContainer__7_4lK")
    return [
        parse_single_course(course, CourseType.FULL_TIME)
        for course in courses
    ]


def get_part_time_courses(part_time_soup: BeautifulSoup) -> [Course]:
    courses = part_time_soup.select(".CourseCard_cardContainer__7_4lK")
    return [
        parse_single_course(course, CourseType.PART_TIME)
        for course in courses
    ]


def get_all_courses() -> list[Course]:
    logging.info("Start parsing...")
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    logging.info("Parsing full-time courses...")
    full_time_soup = soup.select_one("#full-time > .mb-32")

    logging.info("Parsing part-time courses...")
    part_time_soup = soup.select_one("#part-time")

    all_courses = get_full_time_courses(
        full_time_soup
    ) + get_part_time_courses(
        part_time_soup
    )

    return all_courses


def write_courses_to_csv(courses: [Course]) -> None:
    logging.info("Writing to the courses.csv...")
    with open(
            COURSES_OUTPUT_CSV_PATH, "w", encoding="UTF8", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main():
    all_courses = get_all_courses()
    write_courses_to_csv(all_courses)
    logging.info("Done!")


if __name__ == "__main__":
    main()
