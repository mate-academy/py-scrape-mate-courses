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
    link: str
    num_modules: int = 0
    num_topics: int = 0
    duration: str = ""

    def __str__(self) -> str:
        return f"{self.course_type} {self.name} {self.num_modules} " \
               f"modules {self.num_topics} topics, " \
               f"duration {self.duration} " \
               f"({self.short_description})"


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".DropdownCoursesList_coursesList__xjALB")
    num_courses = get_num_courses(soup)
    print(f"Total courses in academy is {num_courses}")
    courses = get_courses_info(soup)
    for course in courses:
        add_data_to_course(course)
    return courses


def add_data_to_course(course: Course) -> None:
    page = requests.get(BASE_URL + course.link).content
    soup = BeautifulSoup(page, "html.parser")
    course_info = soup.select_one(".typography_landingP2__KdC5Q")
    course.short_description = course_info.text
    course_info = soup.select_one(".CourseModulesHeading_headingGrid__50qAP")
    course.num_modules = int(course_info.contents[0].text.split()[0])
    course.num_topics = int(course_info.contents[1].text.split()[0])
    if len(course_info.contents) > 2:
        course.duration = course_info.contents[2].text
    else:
        course.duration = "free time"


def get_courses_info(page_soup: BeautifulSoup) -> list:
    courses = page_soup.select(".DropdownCoursesList_coursesList__xjALB")
    all_courses = []
    type_of_course = CourseType.FULL_TIME
    for el in courses:
        for content in el.contents:
            all_courses.append(Course(name=content.text,
                                      short_description=content.text,
                                      course_type=type_of_course,
                                      link=content.a.attrs["href"]))
        type_of_course = CourseType.PART_TIME
    return all_courses


def get_num_courses(page_soup: BeautifulSoup) -> int:
    tags = page_soup.select(".DropdownCoursesList_coursesListItem__5fXRO")

    if tags is None:
        return 0

    return len(tags)


def main() -> None:
    courses = get_all_courses()
    for course in courses:
        print(course)


if __name__ == "__main__":
    main()
