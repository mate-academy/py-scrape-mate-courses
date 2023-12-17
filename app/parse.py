from dataclasses import dataclass, astuple
from enum import Enum
import csv

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


def get_all_courses(soup: BeautifulSoup) -> list[Course]:
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course in courses:
        all_courses.extend(get_single_course(course))
    return all_courses


def to_csv(courses: list[Course]) -> None:
    with open("couses.csv", "a") as fh:
        writer = csv.writer(fh, delimiter=",")
        writer.writerow(vars(courses[0]))
        writer.writerows([astuple(course) for course in courses])


def main() -> None:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    to_csv(get_all_courses(soup))


if __name__ == "__main__":
    main()
