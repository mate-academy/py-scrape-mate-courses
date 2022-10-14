import logging
import sys
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

MATE_ACADEMY_URL = "https://mate.academy/"

logging.basicConfig(
    level=logging.DEBUG,
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
    modules_number: str
    topics_number: str
    month_duration: str


def parse_single_course(course_soup: Tag) -> Course:
    logging.info("Starting parsing new course.")

    course_name = (course_soup
                   .select_one(".typography_landingH3__vTjok")
                   .text[5:])

    course_desc = (course_soup
                   .select_one(".CourseCard_courseDescription__Unsqj")
                   .text)

    course_type = CourseType.FULL_TIME

    if "Вечірній" in course_name:
        course_name = course_name[:-9]
        course_type = CourseType.PART_TIME

    detail_url = urljoin(MATE_ACADEMY_URL,
                         course_soup.select_one(".mb-16")["href"])

    detail_page = requests.get(detail_url).content
    detail_soup = BeautifulSoup(detail_page, "html.parser")

    details_element = ".CourseModulesHeading_text__EdrEk"

    modules_number = detail_soup.select(details_element)[0].text.split()[0]

    topics_number = detail_soup.select(details_element)[1].text.split()[0]
    try:
        month = detail_soup.select(details_element)[2].text.split()[0]
    except IndexError:
        month = "No data"

    logging.info(f"Successfully parsed {course_name}.")
    return Course(
        name=course_name,
        short_description=course_desc,
        course_type=course_type,
        modules_number=modules_number,
        topics_number=topics_number,
        month_duration=month,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_ACADEMY_URL).content
    soup = BeautifulSoup(page, "html.parser")
    course_containers = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in course_containers]


if __name__ == "__main__":
    get_all_courses()
