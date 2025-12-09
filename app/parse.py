from __future__ import annotations
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag
import csv


URL = "https://mate.academy"


def get_html(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int = 0


def safe_get_text(element: Tag | None) -> str:
    return element.get_text(strip=True) if element else ""


def parse_courses(course_block: Tag) -> Course:
    name_el = course_block.select_one("h3.ProfessionCard_title__m7uno")
    desc_el = course_block.select_one("p.ProfessionCard_description__K8weo")
    duration_el = course_block.select_one("p.ProfessionCard_duration__13PwX")

    return Course(
        name=safe_get_text(name_el),
        short_description=safe_get_text(desc_el),
        duration=safe_get_text(duration_el),
    )


def get_all_courses() -> list[Course]:
    url = f"{URL}/courses"
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    courses = []
    for block in soup.select("div.ProfessionCard_content__mPiVi"):
        courses.append(parse_courses(block))

    return courses


def save_courses_to_csv(courses: list[Course], output_csv_path: str) -> None:
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "short_description", "duration", "modules_count"])
        for course in courses:
            writer.writerow([
                course.name,
                course.short_description,
                course.duration,
                course.modules_count,
            ])


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    save_courses_to_csv(courses, output_csv_path)


if __name__ == "__main__":
    main("courses.csv")
