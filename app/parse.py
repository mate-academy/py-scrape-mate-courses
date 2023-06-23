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


def get_all_courses() -> list[Course]:
    list_of_courses = []

    re = requests.get("https://mate.academy")
    soup = BeautifulSoup(re.text, "html.parser")
    for el in soup.select("#all-courses"):
        for full_time in el.select("#full-time"):
            for course in full_time.select("div > section"):
                list_of_courses.append(
                    Course(
                        name=course.span.text,
                        short_description=course.p.text,
                        course_type=CourseType.FULL_TIME,
                    )
                )
        for part_time in el.select("#part-time"):
            for course in part_time.select("div > section"):
                list_of_courses.append(
                    Course(
                        name=course.span.text,
                        short_description=course.p.text,
                        course_type=CourseType.PART_TIME,
                    )
                )
    return list_of_courses
