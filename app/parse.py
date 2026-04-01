import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int
    topics_count: int


def create_course_link(url: str) -> str:
    full_link = BASE_URL + url
    return full_link


def get_num_of_topics_per_module(module: BeautifulSoup) -> int:
    content = module.find_next(
        "div", class_="CourseModulesList_content__RciF7")
    topics_per_module = content.select(
        "li.CourseModulesList_topicItem__8wNTG") if content else []
    return len(topics_per_module)


def get_num_of_topics_per_course(url: str) -> int:
    full_link = create_course_link(url)
    response = requests.get(full_link).content
    topics_per_course = 0
    page_soup = BeautifulSoup(response, "html.parser")
    modules = page_soup.select("div.CourseModulesList_moduleListItem__b8AY9")
    for module in modules:
        topics_per_course += get_num_of_topics_per_module(module)
    return topics_per_course


def get_num_of_modules_per_course(url: str) -> int:
    full_link = create_course_link(url)
    response = requests.get(full_link).content
    page_soup = BeautifulSoup(response, "html.parser")
    modules = page_soup.select("div.CourseModulesList_moduleListItem__b8AY9")
    return len(modules)


def get_one_course(card: BeautifulSoup) -> Course:
    name = card.select_one("h3.ProfessionCard_title__m7uno span").text
    short_description = card.select_one(
        "p.ProfessionCard_description__K8weo").text
    duration = card.select_one("p.ProfessionCard_duration__13PwX").text
    module_link = card["href"]
    modules_count = get_num_of_modules_per_course(module_link)
    topics_count = get_num_of_topics_per_course(module_link)

    return Course(
        name=name,
        short_description=short_description,
        duration=duration,
        modules_count=modules_count,
        topics_count=topics_count
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(response, "html.parser")
    cards = page_soup.select("a.ProfessionCard_cardWrapper__BCg0O")
    courses = []
    for card in cards:
        courses.append(get_one_course(card))
    return courses


if __name__ == "__main__":
    print(get_all_courses())
