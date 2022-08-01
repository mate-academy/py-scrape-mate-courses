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
    type: CourseType


def get_single_course(course):
    name = course.select_one('.typography_landingH3__vTjok').text
    description = course.select_one('p').text
    if "Вечірній" in name:
        course_type = "part-time"
    else:
        course_type = "full-time"
    course = Course(name=name, short_description=description, type=course_type)
    return course


def get_all_courses():
    courses_response = requests.get(BASE_URL).content
    soup = BeautifulSoup(courses_response, "html.parser")
    all_courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [get_single_course(course) for course in all_courses]


for course in get_all_courses():
    print(f"{course.name}, {course.short_description}, {course.type}")
