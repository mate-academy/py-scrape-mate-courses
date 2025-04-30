from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

HOME_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_single_course(soup: Tag) -> Course:
    return Course(
        name=soup.select_one(".ProfessionCard_title__m7uno").text,
        short_description=soup.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=soup.select_one(".ProfessionCard_duration__13PwX").text,
    )


def get_all_courses() -> list[Course]:
    text = requests.get(HOME_URL).content
    soup_data = BeautifulSoup(text, "html.parser")
    courses = soup_data.select(".ProfessionCard_content__mPiVi")
    return [get_singe_course(course) for course in courses]


if __name__ == "__main__":
    print(get_all_courses())
