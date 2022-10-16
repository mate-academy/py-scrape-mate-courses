from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/ru"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    count_of_modules: str
    count_of_topics: str
    duration: str
    course_type: CourseType


def additional_info(url: str) -> list:
    course_url = urljoin(BASE_URL, url)
    about_course = requests.get(course_url).content
    soup = BeautifulSoup(about_course, "html.parser")
    info = soup.select_one(".CourseModulesHeading_headingGrid__50qAP")
    return [el.p.text for el in info]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")
    all_courses = page_soup.select(".CourseCard_cardContainer__7_4lK")
    name = ".typography_landingH3__vTjok"
    description = ".CourseCard_courseDescription__Unsqj"
    return [
        Course(name=course.select_one(name).text.strip(),
               short_description=course.select_one(description).text.strip(),
               course_type=CourseType.PART_TIME
               if course.select("[rel=nofollow]")
               else CourseType.FULL_TIME,
               count_of_modules=additional_info(course.a["href"])[0],
               count_of_topics=additional_info(course.a["href"])[1],
               duration=additional_info(course.a["href"])[2]
               if len(additional_info(course.a["href"])) > 2 else None,
               ) for course in all_courses

    ]
