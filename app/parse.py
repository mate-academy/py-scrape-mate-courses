from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_courses_by_course_type(course_type: CourseType) -> list[Course]:
    courses_list = []
    request = requests.get(BASE_URL).content
    soup = BeautifulSoup(request, "html.parser")
    soup_full = soup.find(id=course_type.value)
    courses = soup_full.select(".CourseCard_cardContainer__7_4lK")
    for course in courses:
        name = course.select_one(".typography_landingH3__vTjok").text
        short_description = course.select_one(".CourseCard_courseDescription__Unsqj").text
        courses_list.append(Course(name, short_description, course_type))
    return courses_list


def get_all_courses() -> list[Course]:
    courses_list = []
    for course_type in CourseType:
        courses_list += get_courses_by_course_type(course_type)
    return courses_list


if __name__ == '__main__':
    get_all_courses()
