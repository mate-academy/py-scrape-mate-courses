import logging
import sys
from dataclasses import dataclass
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("parser.log"),
    ],
)

BASE_URL = "https://mate.academy/"


class ParseError(Exception):
    pass


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules: list[str]


def get_html(url: str) -> BeautifulSoup:
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        logging.error(e)
        raise ParseError
    if response.status_code != 200:
        logging.error(f"Status code: {response.status_code}")
        raise ParseError
    return BeautifulSoup(response.content, "html.parser")


def get_course_description(soup: BeautifulSoup) -> str:
    element = soup.select_one(".SalarySection_aboutProfession__C6ftM")
    if element is None:
        logging.error(f"Element not found")
        raise ParseError
    return element.get_text()


def get_single_module(module: Tag) -> str:
    name = module.select_one(".CourseModulesList_topicName__7vxtk").get_text(
        strip=True
    )
    topics_count = module.select_one(".CourseModulesList_topicsCount__H_fv3")
    if not name:
        name = "N/A"
    if topics_count:
        topics_count = topics_count.get_text(strip=True).split()[0]
    else:
        topics_count = "N/A"
    return f"{name} ({topics_count} topics)"


def get_modules(soup: BeautifulSoup) -> list[str]:
    result = []
    modules = soup.select(
        ".CourseModulesList_modulesList__C86yL > .color-dark-blue"
    )
    # 1st element is a "get started" text
    for module in modules[2:]:
        result.append(get_single_module(module))
    return result


def get_detail_data(detail_url: str) -> tuple[list[str], str]:
    soup = get_html(detail_url)
    modules = get_modules(soup)
    description = get_course_description(soup)
    return modules, description


def get_course(card: Tag) -> Course:
    detail_url = card.get("href", None)
    if not detail_url:
        raise Exception("No detail url found")
    detail_url = urljoin(BASE_URL, detail_url)
    modules, description = get_detail_data(detail_url)
    name = card.select_one(".ProfessionCard_title__m7uno").get_text(
        strip=True
    )
    duration = card.select_one(".typography_paragraphMedium__FWO7K").get_text(
        strip=True
    )
    if not name:
        name = "N/A"
    if not description:
        description = "N/A"

    return Course(
        name=name,
        short_description=description,
        duration=duration,
        modules=modules,
    )


def get_all_courses(url: str = BASE_URL) -> List[Course]:
    soup = get_html(url)
    cards = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    result = []
    for card in cards:
        try:
            result.append(get_course(card))
        except ParseError:
            pass
    return result


def main() -> None:
    courses = get_all_courses(BASE_URL)
    for course in courses:
        print(course)


if __name__ == "__main__":
    main()
