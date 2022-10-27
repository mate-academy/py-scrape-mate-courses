from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

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
    modules: str
    topics: str
    duration: str


def get_single_course(
        course: BeautifulSoup,
        course_type: CourseType
) -> Course:
    name = course.select_one(".typography_landingH3__vTjok").text
    short_description = course.select_one(
        ".CourseCard_courseDescription__Unsqj").text
    course_link = course.select_one(".CourseCard_button__HTQvE").get("href")
    course_url = urljoin(BASE_URL, course_link)
    request = requests.get(course_url).content
    soup = BeautifulSoup(request, "html.parser")
    modules = soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP").text
    topics = soup.select_one(".CourseModulesHeading_topicsNumber__PXMnR").text
    duration = None
    if course_type == CourseType.FULL_TIME:
        duration = soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H").text
    return Course(
        name,
        short_description,
        course_type,
        modules,
        topics,
        duration
    )


def get_courses_by_course_type(course_type: CourseType) -> list[Course]:
    courses_list = []
    request = requests.get(BASE_URL).content
    soup = BeautifulSoup(request, "html.parser")
    soup_type = soup.find(id=course_type.value)
    courses = soup_type.select(".CourseCard_cardContainer__7_4lK")
    for course in courses:
        courses_list.append(get_single_course(course, course_type))
    return courses_list


def get_all_courses() -> list[Course]:
    courses_list = []
    for course_type in CourseType:
        courses_list += get_courses_by_course_type(course_type)
    return courses_list


if __name__ == "__main__":
    get_all_courses()
