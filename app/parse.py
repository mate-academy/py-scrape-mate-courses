from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


HOME_URL = "https://mate.academy/"

# A card is either the marked element itself (when it holds the course
# fields) or the parent of a marked element that holds only the image.
COURSE_CARD_SELECTOR = (
    "[data-qa='profession-card']:has([class*='_title']), "
    ":has(> [data-qa='profession-card']:not(:has([class*='_title'])))"
)


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def get_text(card: Tag, selector: str) -> str:
    return card.select_one(selector).get_text(strip=True)


def parse_single_course(card: Tag) -> Course:
    return Course(
        name=get_text(card, "[class*='_title']"),
        short_description=get_text(card, "[class*='_description']"),
        duration=get_text(card, "[class*='_duration']"),
    )


def get_all_courses() -> list[Course]:
    soup = get_soup(HOME_URL)
    cards = soup.select(COURSE_CARD_SELECTOR)
    return [parse_single_course(card) for card in cards]


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
