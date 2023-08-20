from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_one_course(course: Tag) -> Course:
    course_name = course.select_one("a.mb-16")
    course_description = course.select_one("p").text
    course_instance = Course(
        name=course_name.text.replace("Курс ", ""),
        short_description=course_description,
        course_type=(
            CourseType.PART_TIME
            if "parttime" in course_name["href"]
            else CourseType.FULL_TIME
        ),
    )
    return course_instance


def get_all_courses() -> list[Course]:
    content = requests.get(BASE_URL).content
    soup = BeautifulSoup(content, "html.parser")

    all_courses_list = []

    courses = soup.select("section.CourseCard_cardContainer__7_4lK")

    for course in courses:
        one_course = get_one_course(course)
        all_courses_list.append(one_course)

    return all_courses_list


if __name__ == "__main__":
    get_all_courses()
