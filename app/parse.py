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
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    headers = {"User-Agent": user_agent}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    courses = []

    cards = soup.find_all(class_=lambda x: x and "CourseCard_card" in x)
    if not cards:
        cards = soup.find_all("a", href=lambda x: x and "/courses/" in x)

    for card in cards:
        name_elem = (
            card.find(attrs={"data-qa": "profession-title"})
            or card.find("span", class_=lambda x: x and "headlineSix" in x)
            or card.find(["h3", "span"])
        )

        desc_elem = card.find(class_=lambda x: x and "Typography_caption" in x)
        dur_elem = card.find(class_=lambda x: x and "CourseCard_duration" in x)

        if name_elem:
            name_text = name_elem.get_text(strip=True)
            if name_text and len(name_text) > 2:
                courses.append(Course(
                    name=name_text,
                    short_description=(
                        desc_elem.get_text(strip=True) if desc_elem else ""
                    ),
                    duration=dur_elem.get_text(strip=True) if dur_elem else ""
                ))

    unique_courses = []
    seen_names = set()
    for course in courses:
        if course.name not in seen_names:
            unique_courses.append(course)
            seen_names.add(course.name)

    return unique_courses
