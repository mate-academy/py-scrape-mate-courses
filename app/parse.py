from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


URL = "https://mate.academy/"


def get_one_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(".ProfessionCard_title__m7uno").text,
        short_description=course.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=course.select_one(".ProfessionCard_duration__13PwX").text
    )


def get_all_courses() -> list[Course]:

    text = requests.get(URL).content
    page_parse = BeautifulSoup(text, "html.parser")
    parse_courses = page_parse.select(".ProfessionCard_content__mPiVi")

    result = []
    for parse_course in parse_courses:
        result.append(get_one_course(parse_course))

    return result


if __name__ == "__main__":
    get_all_courses()
