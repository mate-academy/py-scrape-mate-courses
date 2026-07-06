from dataclasses import dataclass, fields
import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSES_URL = "https://mate.academy"


COURSES_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(
            ".ProfessionCard_title__m7uno"
        ).text,
        short_description=course.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=course.select_one(
            ".ProfessionCard_duration__13PwX"
        ).text
    )


def get_all_courses() -> list[Course]:
    response = requests.get(COURSES_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    return [parse_single_course(course) for course in courses]


if __name__ == "__main__":
    get_all_courses()
