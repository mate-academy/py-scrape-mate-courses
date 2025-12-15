from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one('h3[class*="ProfessionCard_title"]').text,
        short_description=course.select_one(
            'p[class*="ProfessionCard_description"]'
        ).text,
        duration=course.select_one('p[class*="ProfessionCard_duration"]').text,
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")
    courses_elements = soup.select('a[class*="ProfessionCard_cardWrapper"]')
    return [parse_single_course(course) for course in courses_elements]
