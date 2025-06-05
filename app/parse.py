from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    topics_count: int
    modules_count: int


def soup_parser(tag: str, url: str | None = None) -> list:
    home_url = urljoin(BASE_URL, url)
    text = requests.get(home_url).content
    soup = BeautifulSoup(text, "html.parser")
    return soup.select(tag)


def validate_data(data: Tag) -> str:
    if data:
        return data.text
    return "Not found any information"


def parse_single_course(course: Tag) -> Course:
    url = course.get("href")

    topics_count_list = soup_parser(
        tag=".FactBlockIcon_indigo__yH9KL > .FactBlockIcon_factNumber__FTmxv",
        url=url
    )
    topics_count = int(topics_count_list[0].text)

    modules_list = soup_parser(
        url=url,
        tag="ul.CourseModulesList_modulesList__C86yL > li.color-dark-blue"
    )
    modules_count = len(modules_list)

    name = validate_data(
        course.select_one(".ProfessionCard_title__m7uno")
    )
    duration = validate_data(
        course.select_one(".ProfessionCard_duration__13PwX")
    )

    short_description = validate_data(
        course.select_one(".ProfessionCard_description__K8weo")
    )

    return Course(
        name=name,
        short_description=short_description,
        duration=duration,
        topics_count=topics_count,
        modules_count=modules_count
    )


def get_all_courses() -> list[Course]:

    courses = soup_parser(".ProfessionCard_cardWrapper__BCg0O")
    return [parse_single_course(course) for course in courses]


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
