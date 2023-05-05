import json
from dataclasses import dataclass
from enum import Enum
from typing import List

import requests
from bs4 import BeautifulSoup

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_dict: dict) -> Course:
    name = course_dict['nameShort({"domain":"ua","lang":"uk"})']
    is_part_time = name.split()[-1] == "Вечірній"

    return Course(
        name=name,
        short_description=course_dict["description"],
        course_type=(
            CourseType.PART_TIME if is_part_time else CourseType.FULL_TIME
        )
    )


def parse_courses_from_script_data(data: dict) -> List[Course]:

    courses_data = [val for key, val in data.items() if key.startswith("Course")]

    return [parse_single_course(course) for course in courses_data]


def get_all_courses() -> List[Course]:
    req = requests.get(URL)
    soup = BeautifulSoup(req.content, "html.parser")
    script = soup.select_one("#__NEXT_DATA__")
    data = dict(json.loads(script.text))["props"]["apolloState"]
    courses = parse_courses_from_script_data(data)

    return courses


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
