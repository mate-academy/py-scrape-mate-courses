import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass
from enum import Enum


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(soup: BeautifulSoup) -> [Course]:
    result = [Course(
        name=soup.select_one(".ProfessionCard_cardWrapper__JQBNJ"
                             " > a > h3").text,
        short_description=soup.select_one(".ProfessionCard_cardWrapper__JQBNJ"
                                          " > .mb-32").text,
        course_type=CourseType.PART_TIME
    )]

    if soup.select_one("a[data-qa='fulltime-course-more-details-button']"):
        result.append(Course(
            name=soup.select_one(".ProfessionCard_cardWrapper__JQBNJ"
                                 " > a > h3").text,
            short_description=soup.select_one(".ProfessionCard_cardWrapper"
                                              "__JQBNJ"
                                              " > .mb-32").text,
            course_type=CourseType.FULL_TIME
        ))

    return result


def get_courses_soups(page_soup: BeautifulSoup) -> [BeautifulSoup]:
    return page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_soups = get_courses_soups(soup)

    return [
        course
        for course_soup in courses_soups
        for course in parse_single_course(course_soup)
    ]
