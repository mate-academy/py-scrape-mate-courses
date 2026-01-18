from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    response = requests.get("https://mate.academy/")
    response.raise_for_status()

    parser = BeautifulSoup(response.content, "html.parser")

    courses = []

    for course in parser.select(
        "a.ProfessionCard_cardWrapper__BCg0O"
        ".ProfessionsListSectionTemplate_card__ZNsgf"
    ):
        name = course.select_one("h3")
        name = name.text if name else ""

        short_description = course.select("p")[-1].text
        duration = course.select_one("p").text

        courses.append(
            Course(
                name=name,
                short_description=short_description,
                duration=duration
            )
        )

    return courses
