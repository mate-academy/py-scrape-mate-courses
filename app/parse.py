import csv
import logging
import sys
from dataclasses import dataclass, fields, astuple
from datetime import datetime
from enum import Enum

import requests
from bs4 import BeautifulSoup


HOME_URL = "https://mate.academy/"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


CSV_FIELDS_COURSE = [field.name for field in fields(Course)]


def get_course_type(course_soup: BeautifulSoup) -> [CourseType]:
    tags = course_soup.select(".ButtonBody_buttonText__FMZEg")
    course_types = []
    for tag in tags:

        if tag.text == "Власний темп":
            course_types.append(CourseType("part-time"))

        if tag.text == "Повний день":
            course_types.append(CourseType("full-time"))

    return course_types


def get_page_soup() -> BeautifulSoup:
    page = requests.get(HOME_URL).content
    return BeautifulSoup(page, "html.parser")


def parse_single_course(
    course_soup: BeautifulSoup, course_type: [CourseType]
) -> Course:
    return Course(
        name=course_soup.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course_soup.select_one(
            ".typography_landingTextMain__Rc8BD"
        ).text,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    logging.info(
        f"Started parsing at {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}"
    )
    page_soup = get_page_soup()
    course_cards = page_soup.select("div.ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []

    for number, course_card in enumerate(course_cards):
        logging.info(f"Processing {number + 1} of {len(course_cards)} items.")
        course_types = get_course_type(course_card)
        for course_type in course_types:
            all_courses.append(parse_single_course(course_card, course_type))

    logging.info(
        f"Finished parsing at {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}"
    )

    return all_courses


def output_as_csv(
        path: str,
        obj_to_write: [Course],
        csv_fields: list[str]
) -> None:
    with open(path, "w",) as file:
        writer = csv.writer(file)
        writer.writerow(csv_fields)
        writer.writerows([astuple(obj) for obj in obj_to_write])

    logging.info(f"Saved {len(obj_to_write)} objects to {path}.")


if __name__ == "__main__":
    logging.info(f"Server response: {requests.get(HOME_URL).status_code}")
    courses = get_all_courses()
    output_as_csv("output.csv", courses, CSV_FIELDS_COURSE)
