from dataclasses import dataclass

from pip._vendor import requests
from bs4 import BeautifulSoup, Tag

mate_url = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    module_count: str
    topic_count: str


def get_soup(mate_url: str) -> Tag:
    response = requests.get(mate_url).content
    soup = BeautifulSoup(response, "html.parser")
    return soup


def get_module_topic_count(cart_detail_soup: Tag) -> tuple:
    topic_count = cart_detail_soup.select_one(
        ".CourseProgram_card__p5TPZ .FactBlockIcon_factNumber__FTmxv"
    ).text
    module_count = len(cart_detail_soup.select(
        ".CourseModulesList_modulesList__C86yL .color-dark-blue"
    ))
    return module_count, topic_count


def get_course(course_soup: Tag) -> Course:
    cart_detail_url = course_soup["href"]
    cart_detail_soup = get_soup(f"{mate_url}{cart_detail_url}")
    module_count, topic_count = get_module_topic_count(cart_detail_soup)
    return Course(
        name=course_soup.select_one(".ProfessionCard_title__m7uno").text,
        short_description=course_soup.
        select_one(".ProfessionCard_description__K8weo").text,
        duration=course_soup.
        select_one(".ProfessionCard_duration__13PwX").text[0],
        module_count=module_count,
        topic_count=topic_count
    )


def get_all_courses() -> list[Course]:
    result = []
    soup = get_soup(mate_url)
    all_courses_soup = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    for course_soup in all_courses_soup:
        result.append(get_course(course_soup))
    return result
