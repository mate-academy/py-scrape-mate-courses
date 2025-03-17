import csv
from dataclasses import dataclass, fields, astuple

from bs4 import BeautifulSoup, Tag
import requests


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(soup: Tag) -> Course:
    return Course(
        name=soup.select_one(".ProfessionCard_title__m7uno").text,
        short_description=soup.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=soup.select_one(".ProfessionCard_duration__13PwX").text
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(response, "html.parser")
    courses = page_soup.select(".ProfessionCard_content__mPiVi")
    return [parse_single_course(course) for course in courses]


def write_courses_to_csv(output_csv_path: str, courses: [Course]) -> None:
    with open(
            f"{output_csv_path}",
            "w",
            encoding="utf-8",
            newline=""
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main(output_csv_path: str) -> None:
    write_courses_to_csv(output_csv_path, get_all_courses())


if __name__ == "__main__":
    main("courses.csv")
