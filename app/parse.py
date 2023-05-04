from dataclasses import dataclass
from enum import Enum
import json
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
    name = course_dict.get('nameShort({"domain":"ua","lang":"uk"})')
    if not name:
        return None

    part_time = "вечірній" in name.lower()
    return Course(
        name=name,
        short_description=course_dict.get("description") or "",
        course_type=(
            CourseType.PART_TIME if part_time else CourseType.FULL_TIME
        ),
    )


def get_all_courses() -> [Course]:
    try:
        req = requests.get("https://mate.academy/")
        req.raise_for_status()
        soup = BeautifulSoup(req.content, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            return []
        data = json.loads(script.string)["props"]["apolloState"]
        courses = [
            value for key, value in data.items() if key.startswith("Course")
        ]

        return [
            course for course in map(parse_single_course, courses) if course
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching courses: {e}")
        return []


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
