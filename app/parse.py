from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag


MATE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def check_full_time_course_exists(course: Tag) -> bool:
    if course.select_one(
            "a[data-qa=fulltime-course-more-details-button]"
    ) is not None:
        return True
    return False


def check_part_time_course_exists(course: Tag) -> bool:
    if course.select_one(
            "a[data-qa=parttime-course-more-details-button]"
    ) is not None:
        return True
    return False


def get_single_course(course: Tag) -> list[Course]:
    courses = []
    if check_part_time_course_exists(course):
        courses.append(
            Course(
                name=course.select_one(".ProfessionCard_title__Zq5ZY").text,
                short_description=course.select(
                    ".typography_landingTextMain__Rc8BD"
                )[1].text,
                course_type=CourseType.PART_TIME
            )
        )
    if check_full_time_course_exists(course):
        courses.append(
            Course(
                name=course.select_one(".ProfessionCard_title__Zq5ZY").text,
                short_description=course.select(
                    ".typography_landingTextMain__Rc8BD"
                )[1].text,
                course_type=CourseType.FULL_TIME
            )
        )
    return courses


def get_all_courses() -> list[Course]:
    page = requests.get(MATE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")

    courses = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []

    for course in courses:
        all_courses.extend(get_single_course(course))

    return all_courses
