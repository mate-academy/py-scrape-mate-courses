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


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules: list[str]


def get_html(url: str) -> BeautifulSoup:
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def get_course_description(soup: BeautifulSoup) -> str:
    element = soup.select_one(".SalarySection_aboutProfession__C6ftM")
    return element.get_text()


def get_single_module(module: Tag) -> str:
    name = module.select_one(".CourseModulesList_topicName__7vxtk").get_text()
    topics_count = module.select_one(".CourseModulesList_topicsCount__H_fv3")
    if topics_count:
        tasks_count = topics_count.get_text().split()[0]
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
        except Exception as e:
            logging.error(e)
    return [get_course(card) for card in cards]


def main() -> None:
    courses = get_all_courses(BASE_URL)
    for course in courses:
        print(course)


if __name__ == "__main__":
    main()
