from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(name: str, description: str) -> Course:
    course_type = (
        CourseType.PART_TIME if "part" in name else CourseType.FULL_TIME
    )

    return Course(
        name=name.split("-")[0],
        short_description=description,
        course_type=course_type
    )


def parse_single_page(page: str) -> Course:
    page_content = requests.get(page).content
    soup = BeautifulSoup(page_content, "html.parser")
    description = soup.select_one("head title").text
    name = page.split("/")[-1]

    return get_single_course(name=name, description=description)


def generate_parse_pages(page_links: list) -> list[Course]:
    return [*map(parse_single_page, page_links)]


def get_list_page_course(soup: BeautifulSoup, page_url: str) -> list[urljoin]:
    links = soup.select(".large-8 a")
    return [urljoin(page_url, link["href"]) for link in links]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    page_links = get_list_page_course(soup, BASE_URL)
    list_parse_of_courses = generate_parse_pages(page_links)

    return list_parse_of_courses


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
