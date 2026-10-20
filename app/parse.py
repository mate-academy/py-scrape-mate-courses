import csv
import dataclasses
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSE_FIELDS = [field.name for field in dataclasses.fields(Course)]


HOME_URL = "https://mate.academy/"


def parse_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(
            ".FUm52q_title.GPhfBW_captionLarge._70a6ca_captionMedium span"
        ).get_text(strip=True),
        short_description=course.select_one(
            ".GPhfBW_paragraphMedium.FUm52q_text.FUm52q_description"
        ).get_text(strip=True),
        duration=course.select_one(
            ".GPhfBW_paragraphMedium.FUm52q_text.FUm52q_duration"
        ).get_text(strip=True),
    )


def get_all_courses() -> list[Course]:
    response = requests.get(HOME_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    courses = soup.select(".FUm52q_cardWrapper.-j8jFG_card")
    return [parse_course(course) for course in courses]


def write_course(path_name: str, courses: list[Course]) -> None:
    with open(path_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COURSE_FIELDS)
        writer.writerows(dataclasses.astuple(course) for course in courses)


if __name__ == "__main__":
    courses = get_all_courses()
    write_course("courses.csv", courses)
