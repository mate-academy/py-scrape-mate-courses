import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    url = "https://mate.academy/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    courses = []

    course_cards = soup.find_all(
        "a", class_="ProfessionCard_cardWrapper__BCg0O"
    )

    for card in course_cards:
        name_tag = card.find(class_="ProfessionCard_title__m7uno")
        name = name_tag.get_text(strip=True) if name_tag else "N/A"

        desc_tag = card.find(class_="ProfessionCard_description__K8weo")
        short_description = desc_tag.get_text(
            strip=True
        ) if desc_tag else "N/A"

        duration_tag = card.find(class_="ProfessionCard_duration__13PwX")
        duration = duration_tag.get_text(strip=True) if duration_tag else "N/A"

        courses.append(Course(name, short_description, duration))

    return courses


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
