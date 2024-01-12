from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_course_info(course: Tag) -> [Course]:
    course_types = course.select(
        "div.ProfessionCard_buttons__a0o60 > a.Button_fullWidth___Ft6W"
    )
    types = []
    for type_ in course_types:
        if type_.text == "Власний темп":
            types.append(CourseType.PART_TIME)
        else:
            types.append(CourseType.FULL_TIME)
    return [Course(
        name=course.select_one(
            "a.typography_landingH3__vTjok > h3"
        ).text,
        short_description=course.select(
            "p.typography_landingTextMain__Rc8BD"
        )[1].text,
        course_type=type_
    ) for type_ in types]


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_div = soup.select(
        "div.ProfessionCard_cardWrapper__JQBNJ"
    )
    courses = []
    for course in courses_div:
        courses.extend(get_course_info(course))
    return courses


print(get_all_courses())
