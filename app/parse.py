from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
import requests


BASE_URl = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_one_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(".FUm52q_title").get_text(strip=True),
        short_description=(
            course
            .select_one(".FUm52q_description")
            .get_text(strip=True)
        ),
        duration=course.select_one(".FUm52q_duration").get_text(strip=True),
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URl)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    courses = soup.select(".FUm52q_cardWrapper")
    return [parse_one_course(course) for course in courses]


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
