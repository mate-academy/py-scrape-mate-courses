from dataclasses import dataclass
from enum import Enum

import requests
import json
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


BASE_URL = "https://mate.academy"


def parse_page(url: str) -> dict:
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    json_blob = json.loads(script_tag.get_text())
    return dict(json_blob)["props"]["apolloState"]


def get_course_object(course_info: list) -> Course:
    course_object = Course(
        name=course_info[3],
        short_description=course_info[6],
        course_type=(
            CourseType.PART_TIME if "parttime" in course_info[4]
            else CourseType.FULL_TIME
        )
    )
    return course_object


def get_all_courses() -> list[Course]:
    data = parse_page(BASE_URL)
    courses = []
    for key, course_data in data.items():
        if "Course" in key:
            courses.append(list(course_data.values()))
    return [get_course_object(course) for course in courses]
