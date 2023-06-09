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


def parse_all_courses_info() -> tuple[list[str], list[str]]:
    page = requests.get(BASE_URL).text
    soup = BeautifulSoup(page, "html.parser")
    all_names_of_courses = [
        name.text
        for name in soup.find_all(class_="typography_landingH3__vTjok")
    ]
    full_time_courses = [
        course.text
        for course in soup.find_all(class_="cell large-6 large-offset-1 mb-32")
    ]
    part_time_courses = [
        course.text
        for course in soup.find_all(class_="cell large-6 large-offset-1")
    ]
    all_courses_list = full_time_courses + part_time_courses
    all_courses = " ".join(all_courses_list).split("Детальніше")
    all_courses.remove("")

    return all_names_of_courses, all_courses


all_names_courses, all_courses_info = parse_all_courses_info()


def get_all_courses() -> list[Course]:
    all_courses = []

    for i in range(len(all_names_courses)):
        if all_names_courses[i].split()[-1] == "Вечірній":
            course_type = CourseType(CourseType.PART_TIME)

        else:
            course_type = CourseType(CourseType.FULL_TIME)

        course = Course(
            name=all_names_courses[i].replace("Вечірній", "")
            if "Вечірній" in all_names_courses[i]
            else all_names_courses[i],
            short_description=all_courses_info[i].replace(
                f"{all_names_courses[i]}", ""
            ),
            course_type=course_type,
        )

        all_courses.append(course)

    return all_courses


if __name__ == "__main__":
    print(get_all_courses())
