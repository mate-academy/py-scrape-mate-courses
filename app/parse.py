from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    cards = soup.select('a[class*="ProfessionCard_cardWrapper"]')

    courses = []
    for card in cards:
        name = card.select_one(
            'h3[class*="ProfessionCard_title"] span'
        ).text
        duration = card.select_one(
            'p[class*="ProfessionCard_duration"]'
        ).text
        description = card.select_one(
            'p[class*="ProfessionCard_description"]'
        ).text
        courses.append(
            Course(name=name, short_description=description, duration=duration)
        )

    return courses
