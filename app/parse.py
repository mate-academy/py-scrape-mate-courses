import re
from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"

session = requests.Session()


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int | None = None
    topics_count: int | None = None


def get_soup(url: str) -> BeautifulSoup:
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def find_count(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return int(match.group(1)) if match else None


def parse_detail(url: str) -> tuple[int | None, int | None]:
    text = get_soup(url).get_text(" ", strip=True)
    modules_count = find_count(r"(\d+)\s+модул", text)
    topics_count = find_count(r"(\d+)\s+тем", text)
    return modules_count, topics_count


def parse_one_course(course: Tag) -> Course:
    modules_count, topics_count = parse_detail(urljoin(URL, course["href"]))

    return Course(
        name=course.select_one(".FUm52q_title").get_text(strip=True),
        short_description=course.select_one(".FUm52q_description")
        .get_text(strip=True),
        duration=course.select_one(".FUm52q_duration").get_text(strip=True),
        modules_count=modules_count,
        topics_count=topics_count,
    )


def get_all_courses() -> list[Course]:
    soup = get_soup(URL)
    courses = soup.select(".FUm52q_cardWrapper")

    return [parse_one_course(course) for course in courses]


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
