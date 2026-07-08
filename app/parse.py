import pprint
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_single_course(course: BeautifulSoup) -> Course:
    return Course(
        name=course.select_one(
            ".ProfessionCard_title__m7uno"
        ).text,
        short_description=course.select_one(
            ".ProfessionCard_description__K8weo"
        ).text,
        duration=course.select_one(
            ".ProfessionCard_duration__13PwX"
        ).text,
    )


def get_all_courses(url: str) -> list[Course]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    courses_cards = soup.select(
        ".ProfessionCard_content__mPiVi"
    )
    courses = [
        get_single_course(course)
        for course in courses_cards
    ]
    return courses
