from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag
import csv
from typing import List


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


def parse_courses(course_block: Tag) -> Course:
    return Course(
        name=course_block.select_one(
            "h3.ProfessionCard_title__m7uno").text.strip(),
        short_description=course_block.select_one(
            "p.ProfessionCard_description__K8weo").text.strip(),
        duration=course_block.select_one(
            "p.ProfessionCard_duration__13PwX").text.strip(),
    )


def get_all_courses() -> list[Course]:
    courses = []
    url = URL + "/courses"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for course_block in soup.select(
            "div.ProfessionCard_content__mPiVi"):
        courses.append(parse_courses(course_block))
    return courses


def save_courses_to_csv(
        courses: List[Course], output_csv_path: str
) -> None:
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "short_description", "duration"])
        for course in courses:
            writer.writerow([
                course.name,
                course.short_description,
                course.duration])


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    save_courses_to_csv(courses, output_csv_path)


if __name__ == "__main__":
    main("courses.csv")
