import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def fetch_landing_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка завантаження сторінки: {e}")
        return ""


def parse_courses_from_html(html_content: str) -> list[Course]:
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "html.parser")
    courses = []

    cards = soup.select('div[class*="CourseCard_card"]')

    for card in cards:
        name_elem = card.find(attrs={"data-qa": "profession-title"})
        desc_elem = card.find(class_=lambda x: x and "Typography_caption" in x)
        dur_elem = card.find(class_=lambda x: x and "CourseCard_duration" in x)

        if name_elem:
            courses.append(Course(
                name=name_elem.get_text(strip=True),
                short_description=desc_elem.get_text(strip=True) if desc_elem else "",
                duration=dur_elem.get_text(strip=True) if dur_elem else ""
            ))

    return courses


def get_all_courses() -> list[Course]:
    url = "https://mate.academy/"
    html = fetch_landing_html(url)
    all_found = parse_courses_from_html(html)

    unique_courses = []
    seen = set()
    for course in all_found:
        if course.name not in seen:
            unique_courses.append(course)
            seen.add(course.name)

    return unique_courses