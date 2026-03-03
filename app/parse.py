from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag
import requests


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    name = course.select_one("h3").get_text()
    short_description = (
        course.select_one(".ProfessionCard_description_K8weo").get_text())
    duration = course.select_one("p").get_text()
    return Course(name=name,
                  short_description=short_description,
                  duration=duration)


def get_all_courses() -> list[Course]:
    text = requests.get(BASE_URL).content
    soup = BeautifulSoup(text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper_BCg0O")
    return [parse_single_course(course) for course in courses]
