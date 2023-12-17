from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup, Tag
import requests


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(course: Tag) -> [Course]:
    course_name = course.select_one("a").text
    course_description = course.select_one(".mb-32").text

    course_types = {
        "fulltime-course": CourseType.FULL_TIME,
        "parttime-course": CourseType.PART_TIME,
    }

    return [
        Course(
            name=course_name,
            short_description=course_description,
            course_type=course_type,
        ) for class_name, course_type in course_types.items()
        if class_name in str(course)
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course in courses:
        all_courses.extend(get_single_course(course))
    return all_courses


get_all_courses()
