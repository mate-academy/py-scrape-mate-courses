from dataclasses import dataclass
from enum import Enum

import bs4.element
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_modules: int = 0
    num_topics: int = 0
    duration: str = ""

    def __str__(self) -> str:
        return f"{self.course_type} {self.name} {self.num_modules} " \
               f"modules {self.num_topics} topics, " \
               f"duration {self.duration} " \
               f"({self.short_description})"


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL + "/courses").content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    print(f"Total courses in academy is {len(courses)}")
    return [add_data_to_course(course) for course in courses]


def add_data_to_course(course: bs4.element.Tag) -> Course:
    name = course.a.text
    short_description = course.div.text
    type_course = CourseType.FULL_TIME \
        if course.parent.parent.attrs.get("id") == "full-time"\
        else CourseType.PART_TIME

    page = requests.get(BASE_URL + course.a.attrs.get("href")).content
    soup = BeautifulSoup(page, "html.parser")

    course_info = soup.select_one(".CourseModulesHeading_headingGrid__50qAP")
    num_modules = int(course_info.contents[0].text.split()[0])
    num_topics = int(course_info.contents[1].text.split()[0])
    if len(course_info.contents) > 2:
        duration = course_info.contents[2].text
    else:
        duration = "free time"

    return Course(
        name=name,
        short_description=short_description,
        course_type=type_course,
        num_modules=num_modules,
        num_topics=num_topics,
        duration=duration
    )


def get_num_courses(page_soup: BeautifulSoup) -> int:
    tags = page_soup.select(".DropdownCoursesList_coursesListItem__5fXRO")
    return 0 if tags is None else len(tags)


def main() -> None:
    courses = get_all_courses()
    for course in courses:
        print(course)


if __name__ == "__main__":
    main()
