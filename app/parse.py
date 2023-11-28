import logging
import sys
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag


URL = "https://mate.academy/en"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(course_soup: Tag) -> list[Course]:
    courses = []
    name_course = course_soup.select_one("h3").text
    short_description_course = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text
    full_time_button = course_soup.select_one(
        "[data-qa='fulltime-course-more-details-button']"
    )
    part_time_button = course_soup.select_one(
        "[data-qa='parttime-course-more-details-button']"
    )

    if full_time_button:
        courses.append(
            Course(
                name=name_course,
                short_description=short_description_course,
                course_type=CourseType.FULL_TIME
            )
        )

    if part_time_button:
        courses.append(
            Course(
                name=name_course,
                short_description=short_description_course,
                course_type=CourseType.PART_TIME
            )
        )

    return courses


def get_all_courses() -> list[Course]:
    logging.info("Start parsing mate academy")
    page = requests.get(URL).content
    page_soup = BeautifulSoup(page, "html.parser")
    courses = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [course for elem in courses for course in get_single_course(elem)]
