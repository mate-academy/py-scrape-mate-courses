import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_single_course(element: Tag) -> Course:
    name_el = element.select_one(".ProfessionCard_title__m7uno")
    desc_el = element.select_one(".ProfessionCard_description__K8weo")
    duration_el = element.select_one(".ProfessionCard_duration__13PwX")

    name = name_el.get_text(strip=True) if name_el else ""
    short_description = desc_el.get_text(strip=True) if desc_el else ""
    duration = duration_el.get_text(strip=True) if duration_el else ""

    return Course(
        name=name,
        short_description=short_description,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    courses = []
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup.select(".ProfessionCard_content__mPiVi"):
        courses.append(get_single_course(element))

    return courses


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
