from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def safe_get_text(element: Tag, selector: str) -> str:
    node = element.select_one(selector)
    return node.text.strip() if node else ""


def get_course(course: Tag) -> Course:
    return Course(
        name=safe_get_text(course, ".ProfessionCard_title__m7uno"),
        short_description=safe_get_text(
            course,
            ".ProfessionCard_description__K8weo"
        ),
        duration=safe_get_text(course, ".ProfessionCard_duration__13PwX"),
    )


def get_all_courses() -> list[Course]:
    try:
        response = requests.get(BASE_URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {BASE_URL}: {e}")
        return []
    soup_page = BeautifulSoup(response.text, "html.parser")
    courses = soup_page.select(".ProfessionsListSectionTemplate_card__ZNsgf")
    return [get_course(course) for course in courses]


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
