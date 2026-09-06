import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag


URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(".ProfessionCard_title__m7uno").text,
        short_description=course.select_one(".ProfessionCard_description__K8weo").text,
        duration=course.select_one(".typography_paragraphMedium__FWO7K").text
    )


def get_all_courses() -> list[Course]:
    response = requests.get(URL).content
    soup = BeautifulSoup(response, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    all_courses = [parse_single_course(course) for course in courses]

    return all_courses
