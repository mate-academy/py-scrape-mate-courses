from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


URL = "https://mate.academy/#all-courses"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: BeautifulSoup) -> Course:
    return Course(
        name=course.select_one("h3.ProfessionCard_title__m7uno").text.strip(),
        short_description=(
            course.select_one("p.ProfessionCard_description__K8weo")
            .text.strip()
        ),
        duration=(
            course.select_one("p.ProfessionCard_duration__13PwX")
            .text.strip()
        )
    )


def get_all_courses() -> list[Course]:
    text = requests.get(URL).content
    page_soup = BeautifulSoup(text, "html.parser")
    courses = page_soup.select(".ProfessionCard_content__mPiVi")
    return [parse_single_course(course) for course in courses]
