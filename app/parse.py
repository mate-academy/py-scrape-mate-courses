import requests

from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


URL_TO_SCRAPING = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_list_of_courses(blocks: list[Tag]) -> list[Course]:
    courses_data = []

    for block in blocks:
        course_duration = block.select("p")[0].get_text()
        course_name = block.select_one("h3").get_text()
        course_description = block.select("p")[1].get_text()
        courses_data.append(Course(
            name=course_name,
            short_description=course_description,
            duration=course_duration)
        )

    return courses_data


def get_all_courses() -> list[Course]:
    text = requests.get(URL_TO_SCRAPING).content
    soup = BeautifulSoup(text, "html.parser")

    blocks = soup.select(".ProfessionCard_content__mPiVi")

    courses = get_list_of_courses(blocks)
    return courses


if __name__ == "__main__":
    get_all_courses()
