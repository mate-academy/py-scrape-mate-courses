from dataclasses import dataclass
from enum import Enum

import requests
import bs4

URL = "https://www.mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def create_course(card: bs4.element) -> list[Course]:
    courses = []
    part_time = card.find(
        "a", {"data-qa": "parttime-course-more-details-button"}
    )
    full_time = card.find(
        "a", {"data-qa": "fulltime-course-more-details-button"}
    )
    name = card.find("h3").text
    short_description = card.find(
        "p", {"class": "typography_landingTextMain__Rc8BD mb-32"}
    ).text

    if part_time:
        course_type = CourseType.PART_TIME
        course = Course(name, short_description, course_type)
        courses.append(course)

    if full_time:
        course_type = CourseType.FULL_TIME
        course = Course(name, short_description, course_type)
        courses.append(course)

    return courses


def get_all_courses() -> list[Course]:
    courses = []
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    course_cards = soup.findAll(
        "div", {"class": "ProfessionCard_cardWrapper__JQBNJ"}
    )

    for card in course_cards:
        new_courses = create_course(card)
        courses.extend(new_courses)
    return courses


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course.name)
        print(course.short_description)
        print(course.course_type)
        print("------------------------------------")
