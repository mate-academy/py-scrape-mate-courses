from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


URL = "https://mate.academy/"


def fetch_page(url: str) -> bytes:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content


def parse_page() -> list[Tag]:
    soup = BeautifulSoup(fetch_page(URL), "html.parser")

    return soup.find_all("div", class_="FUm52q_content")


def scrape_course(course_info: Tag) -> Course:
    title_tag = course_info.find("span")
    duration_tag = course_info.find(
        "p", class_="GPhfBW_paragraphMedium"
    )
    description_tag = course_info.find(
        "p",
        class_="GPhfBW_paragraphMedium FUm52q_text FUm52q_description"
    )

    name = title_tag.get_text(strip=True) if title_tag else ""
    duration = duration_tag.get_text(strip=True) if duration_tag else ""
    short_description = (
        description_tag.get_text(strip=True)
        if description_tag
        else ""
    )

    return Course(
        name=name,
        short_description=short_description,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    courses = parse_page()
    return [scrape_course(course) for course in courses]
