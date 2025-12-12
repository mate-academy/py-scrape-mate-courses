import requests
import csv
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass, fields, astuple

URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSES_FIELDS = [field.name for field in fields(Course)]


def parser_single_course(course: Tag) -> Course:
    try:
        name = course.select_one(
            ".ProfessionCard_title__m7uno"
        ).get_text(strip=True)
    except AttributeError:
        name = ""

    try:
        short_description = course.select_one(
            ".ProfessionCard_description__K8weo"
        ).get_text(strip=True)
    except AttributeError:
        short_description = ""

    try:
        duration = course.select_one(
            ".ProfessionCard_duration__13PwX"
        ).get_text(strip=True)
    except AttributeError:
        duration = ""
    return Course(
        name=name,
        short_description=short_description,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    text = requests.get(URL).content
    soup = BeautifulSoup(text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    return [parser_single_course(course) for course in courses]


def convert_to_csv(courses: list[Course]) -> None:
    with open("course.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COURSES_FIELDS)
        writer.writerows(astuple(course) for course in courses)


def main() -> None:
    data = get_all_courses()
    convert_to_csv(data)


if __name__ == "__main__":
    main()
