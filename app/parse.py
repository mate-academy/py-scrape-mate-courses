import requests
import csv
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_course(course_block: Tag) -> Course:
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
    url = BASE_URL + "/courses"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for course_block in soup.select(
            "div.ProfessionCard_content__mPiVi"):
        courses.append(parse_course(course_block))
    return courses


def save_courses_to_csv(courses: list[Course], output_csv_path: str) -> None:
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
