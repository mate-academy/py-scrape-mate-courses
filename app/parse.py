import csv
from dataclasses import dataclass, fields, astuple

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/courses/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


FIELDS = [field.name for field in fields(Course)]


def parse_single_course(product: Tag) -> Course:
    name_el = product.select_one(".ProfessionCard_title__m7uno.typography_captionLarge__fZ9ls.typography_medium_captionMedium__MVxkq")  # noqa: E501
    short_el = product.select_one(".typography_paragraphMedium__FWO7K.ProfessionCard_text___l0Du.ProfessionCard_description__K8weo")  # noqa: E501
    duration_el = product.select_one(".typography_paragraphMedium__FWO7K.ProfessionCard_text___l0Du.ProfessionCard_duration__13PwX")  # noqa: E501

    return Course(
        name=name_el.text.strip() if name_el else None,
        short_description=short_el.text.strip() if short_el else None,
        duration=duration_el.text.strip() if duration_el else None,
    )


def get_all_courses() -> list[Course]:
    text = requests.get(BASE_URL).content
    soup = BeautifulSoup(text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    return [parse_single_course(course) for course in courses]


def write_courses_to_csv(courses: list[Course]) -> None:
    with open("courses.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS)
        writer.writerows([astuple(course) for course in courses])


if __name__ == "__main__":
    courses = get_all_courses()
    write_courses_to_csv(courses)
