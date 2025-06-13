from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


BASE_URL = "https://mate.academy/"


def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, "lxml")


def parse_course_elements(soup: BeautifulSoup) -> list[Tag]:
    return soup.select(
        ".ProfessionsListSectionTemplate_cardsWrapper__un6ny "
        "a.ProfessionCard_cardWrapper__BCg0O"
    )


def parse_single_course(course_element: Tag) -> Course:
    name = course_element.select_one("div.ProfessionCard_content__mPiVi h3")
    short_description = course_element.select_one(
        "p.ProfessionCard_description__K8weo"
    )
    duration = course_element.select_one("p.ProfessionCard_duration__13PwX")

    return Course(
        name=name.text.strip(),
        short_description=short_description.text.strip(),
        duration=duration.text.strip(),
    )


def get_all_courses() -> list[Course]:
    soup = fetch_page(BASE_URL)
    course_elements = parse_course_elements(soup)
    return [parse_single_course(course) for course in course_elements]
