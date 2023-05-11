import json
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup


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
    time = CourseType.PART_TIME if name[-1] == "й" else CourseType.FULL_TIME
    return Course(name=name,
                  short_description=course_dict["description"],
                  course_type=time)


def get_all_courses() -> [Course]:
    data = requests.get("https://mate.academy/")
    soup = BeautifulSoup(data.content, "html.parser")
    script = soup.select_one("#__NEXT_DATA__")
    content = dict(json.loads(script.text))["props"]["apolloState"]
    courses = [val for key, val in content.items() if key.startswith("Course")]

    return [parse_single_course(course) for course in courses]


if __name__ == "__main__":
    for i in get_all_courses():
        print(i)
