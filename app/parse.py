import logging
import sys
from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

MATE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def parse_single_course_card(
        course_soup: BeautifulSoup, course_type: CourseType
) -> Course:
    name = course_soup.select_one("a.ProfessionCard_title__Zq5ZY > h3").text
    short_description = course_soup.select_one(
        ".ProfessionCard_cardWrapper__JQBNJ > .mb-32"
    ).text

    logging.info(f"Parsing course {name}, {course_type.value}")

    return Course(
        name=name, short_description=short_description, course_type=course_type
    )


def get_all_courses() -> list[Course]:
    logging.info("Start parsing courses page")

    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    courses_list = []

    for course in courses:
        part_time_course = parse_single_course_card(
            course, CourseType.PART_TIME
        )

        courses_list.append(part_time_course)

        if course.select_one(
                "a[data-qa='fulltime-course-more-details-button']"
        ):
            full_time_course = parse_single_course_card(
                course, CourseType.FULL_TIME
            )
            courses_list.append(full_time_course)

    return courses_list


if __name__ == "__main__":
    print(get_all_courses())
