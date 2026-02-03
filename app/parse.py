from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag, ResultSet

MATE_URL = "https://mate.academy/en"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(".ProfessionCard_title__m7uno > span").text,
        short_description=course
        .select_one(".ProfessionCard_description__K8weo")
        .text,
        duration=course
        .select_one(".ProfessionCard_duration__13PwX")
        .text
        .split()[0]
    )


def scrape_page() -> ResultSet[Tag]:
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")

    return courses


def get_all_courses() -> list[Course]:
    courses = scrape_page()
    return [parse_single_course(course) for course in courses]
