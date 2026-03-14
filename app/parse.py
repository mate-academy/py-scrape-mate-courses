from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.request import urlopen


URL = "https://mate.academy/en/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def fetch_page(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode("utf-8")


def parse_courses(html: str) -> list[Course]:
    soup = BeautifulSoup(html, "html.parser")
    courses: list[Course] = []

    course_cards = soup.select(
        "section a[href*='courses'], "
        "section a[href*='career']"
    )
    for card in course_cards:
        name_tag = card.select_one("h3")
        desc_tag = card.select_one("p")

        name = name_tag.get_text(strip=True) if name_tag else ""
        short_description = desc_tag.get_text(strip=True) if desc_tag else ""

        duration = ""
        text = card.get_text(" ", strip=True)
        words = text.split()

        for i, word in enumerate(words):
            if "+" in word and i + 1 < len(words):  # FIX: prevent IndexError
                if "month" in words[i + 1]:
                    duration = f"{word} {words[i + 1]}"
                    break

        if name:
            courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    duration=duration,
                )
            )

    return courses


def get_all_courses() -> list[Course]:
    html = fetch_page(URL)
    return parse_courses(html)
