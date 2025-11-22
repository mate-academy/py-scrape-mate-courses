from dataclasses import dataclass

import requests
from bs4 import Tag, BeautifulSoup


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def safe_text(element: Tag) -> str:
    return element.get_text(strip=True) if element else ""


def parse_single_course(course: Tag) -> Course:
    name_el = course.select_one("h3.ProfessionCard_title__m7uno")
    desc_el = course.select_one(
        "p.ProfessionCard_description__K8weo"
    )
    duration_el = course.select_one("p.ProfessionCard_duration__13PwX")

    return Course(
        name=safe_text(name_el),
        short_description=safe_text(desc_el),
        duration=safe_text(duration_el),
    )


def get_all_courses() -> list[Course]:
    text = requests.get(BASE_URL).content
    soup = BeautifulSoup(text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")

    return [parse_single_course(course) for course in courses]
