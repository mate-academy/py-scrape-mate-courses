import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(element: Tag) -> Course:
    return Course(
        name=element.select_one(".ProfessionCard_title__m7uno").text,
        short_description=element.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=element.select_one(".ProfessionCard_duration__13PwX").text,
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    course_elements = soup.select(".ProfessionCard_cardWrapper__BCg0O")

    return [parse_single_course(element) for element in course_elements]
