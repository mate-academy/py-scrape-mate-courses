import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: list[str]
    duration: str
    modules: int
    topics: int


def serializer(course: Tag) -> Course:
    name = course.select_one("h3 > span").text
    duration = course.select_one("div > p").text
    description = [item.string for item in course.select("div > div > span")]
    link_pref = course["href"]
    response = requests.get(BASE_URL + link_pref).content
    soup = BeautifulSoup(response, "html.parser")
    modules = len(
        soup.select(".CourseModulesList_modulesList__C86yL > li")) - 1
    topics = [
        int(topic.text[0])
        for topic
        in soup.select(".CourseModulesList_topicsCount__H_fv3")
    ]

    return Course(
        name=name,
        short_description=description,
        duration=duration,
        modules=modules,
        topics=sum(topics),
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    return [serializer(course) for course in courses]


if __name__ == "__main__":
    get_all_courses()
