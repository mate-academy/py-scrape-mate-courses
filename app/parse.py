import logging
import sys
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/en"

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)8s]: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    button_texts = [button.text for button in course_soup.select(".ButtonBody_buttonText__FMZEg")]

    if "Full time" in button_texts:
        course_type = CourseType("full-time")
    elif "Flex" in button_texts:
        course_type = CourseType("part-time")

    return Course(
        name=course_soup.select_one("h3").text,
        short_description=course_soup.select(".typography_landingTextMain__Rc8BD")[-1].text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    logging.info("Start parsing")

    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [parse_single_course(course_soup) for course_soup in courses_soup]


if __name__ == "__main__":
    print(get_all_courses())
