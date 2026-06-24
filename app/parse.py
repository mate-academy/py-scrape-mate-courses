from dataclasses import dataclass


import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules: int
    topics: int


def get_count_modules_and_topics(url: str) -> dict:
    html_content = requests.get(BASE_URL + url).content
    soup = BeautifulSoup(html_content, "html.parser")
    modules = soup.select(".CourseModulesList_topicName__7vxtk")
    topics = [
        int(
            topic.select_one(
                ".CourseModulesList_topicsCount__H_fv3"
            ).text.split()[0]
        )
        for topic in soup.select(".CourseModulesList_itemLeft__BKWFl")
    ]
    return {"modules": len(modules), "topics": sum(topics)}


def get_single_course(course: Course) -> Course:
    course_url = course.get("href")
    modules_and_topics = get_count_modules_and_topics(course_url)
    return Course(
        name=course.select_one(".ProfessionCard_title__m7uno").text,
        short_description=course.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=course.select_one(".ProfessionCard_text___l0Du").text,
        modules=modules_and_topics["modules"],
        topics=modules_and_topics["topics"],
    )


def get_all_courses() -> list[Course]:

    html_content = requests.get(BASE_URL).content
    soup = BeautifulSoup(html_content, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__BCg0O")
    return [get_single_course(course) for course in courses]
