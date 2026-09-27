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
    page.raise_for_status()
    soup = BeautifulSoup(page.content, "html.parser")

    cards = soup.select('a[class*="ProfessionCard_cardWrapper"]')

    courses = []
    for card in cards:
        name_tag = card.select_one('h3[class*="ProfessionCard_title"] span')
        duration_tag = card.select_one('p[class*="ProfessionCard_duration"]')
        description_tag = card.select_one(
            'p[class*="ProfessionCard_description"]'
        )
        if not (name_tag and duration_tag and description_tag):
            continue

        courses.append(
            Course(
                name=name_tag.text,
                short_description=description_tag.text,
                duration=duration_tag.text,
            )
        )

    return courses
