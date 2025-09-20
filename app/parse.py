from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(".ProfessionCard_title__m7uno").text,
        short_description=course.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=course.select_one(".ProfessionCard_duration__13PwX").text
    )


def get_all_courses() -> list[Course]:
    main_page = requests.get(BASE_URL).text
    soup_page = BeautifulSoup(main_page, "html.parser")
    courses = soup_page.select(".ProfessionsListSectionTemplate_card__ZNsgf")
    return [get_course(course) for course in courses]


get_all_courses()
