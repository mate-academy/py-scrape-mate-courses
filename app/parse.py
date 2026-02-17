import csv
from dataclasses import dataclass, fields, astuple
import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one("h3 span").text,
        short_description=course.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=course.select_one(".ProfessionCard_duration__13PwX").text
    )


def get_all_courses() -> list[Course]:
    text = requests.get(URL).content
    soup = BeautifulSoup(text, "html.parser")
    cards = soup.select(".ProfessionCard_content__mPiVi")
    return [parse_single_course(card) for card in cards]


def write_courses_to_csv(courses: list[Course]) -> None:
    with open("result.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main() -> None:
    write_courses_to_csv(get_all_courses())


if __name__ == "__main__":
    main()
