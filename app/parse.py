from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    courses = []

    course_cards = soup.select(".ProfessionCard_content__mPiVi")

    for card in course_cards:
        name = card.select_one(".ProfessionCard_title__m7uno")
        description = card.select_one(".ProfessionCard_description__K8weo")
        duration = card.select_one(".ProfessionCard_duration__13PwX")

        if name and description and duration:
            courses.append(
                Course(
                    name=name.get_text(strip=True),
                    short_description=description.get_text(strip=True),
                    duration=duration.get_text(strip=True),
                )
            )

    return courses
