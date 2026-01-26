import csv
from dataclasses import dataclass, astuple
from pydoc_data.topics import topics

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_one_course(course: BeautifulSoup) -> Course:
    return Course(
        name=course.select_one(
            ".typography_medium_captionMedium__MVxk"
        ).text,
        short_description=course.select_one(
            ".ProfessionCard_description__K8weo"
        ).get_text(),
        duration=course.select_one(
            ".ProfessionCard_duration__13PwX"
        ).text,
    )


def get_all_courses() -> list[Course]:
    text = requests.get(BASE_URL).text
    soup = BeautifulSoup(text, "html.parser")
    courses = soup.select(".ProfessionCard_content__mPiVi")
    return [parse_one_course(course) for course in courses]


def csv_writter(courses: list[Course]) -> None:
    with open("courses.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Short Description", "Duration"])
        writer.writerows(astuple(course) for course in courses)


if __name__ == "__main__":
    csv_writter(get_all_courses())
