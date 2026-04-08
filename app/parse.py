import csv
from dataclasses import (
    dataclass,
    field,
    astuple,
    fields
)
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag
import requests


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int = field(default=0)
    topics_count: int = field(default=0)


COURSE_FIELDS = [field.name for field in fields(Course)]

HOME_URL = "https://mate.academy/"


def fetch_soup(url: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url).text, "html.parser")


def safe_get_text(element: Tag) -> str:
    return element.get_text(strip=True) if element else ""


def get_course_cards(soup: BeautifulSoup) -> list[Tag]:
    container = soup.select_one(
        "div[class*='ProfessionsListSectionTemplate_cardsWrapper']"
    )
    if not container:
        return []

    return container.select("a[href^='/courses/']")


def parse_course_base_info(course: Tag) -> Course:
    return Course(
        name=safe_get_text(course.select_one("h3")),
        short_description=safe_get_text(
            course.select_one("p[class*='ProfessionCard_description']")
        ),
        duration=safe_get_text(
            course.select_one("p[class*='ProfessionCard_duration']")
        ),
    )


def get_modules_list(course_soup: BeautifulSoup) -> list[Tag]:
    modules_list = course_soup.select_one("ul[class*='CourseModulesList']")
    if not modules_list:
        return []

    return modules_list.find_all("li", recursive=False)


def count_modules_and_topics(modules: list[Tag]) -> tuple[int, int]:
    topics_total = 0

    for module in modules:
        text = safe_get_text(module.select_one("p[class*='topicsCount']"))
        if text:
            topics_total += int(text.split()[0])

    return len(modules), topics_total


def enrich_course_with_details(course: Course, course_url: str) -> None:
    soup = fetch_soup(course_url)
    modules = get_modules_list(soup)

    modules_count, topics_count = count_modules_and_topics(modules)

    course.modules_count = modules_count
    course.topics_count = topics_count


def get_all_courses() -> list[Course]:
    soup = fetch_soup(HOME_URL)
    course_cards = get_course_cards(soup)

    courses: list[Course] = []

    for card in course_cards:
        course = parse_course_base_info(card)

        course_url = urljoin(HOME_URL, card["href"])
        enrich_course_with_details(course, course_url)

        courses.append(course)

    return courses


def write_courses_to_csv(courses: list[Course]) -> None:
    with open("results.csv", "w", newline="", encoding="utf-8") as _file:
        writer = csv.writer(_file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


if __name__ == "__main__":
    write_courses_to_csv(get_all_courses())
