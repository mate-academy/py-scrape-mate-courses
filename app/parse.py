from dataclasses import dataclass
from enum import Enum
from typing import Any

import requests
from bs4 import BeautifulSoup

BASE_HOST = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: Any
) -> [Course]:
    soup_courses = course_soup.select("span.typography_landingH3__vTjok")
    soup_description = course_soup.select("div p")[3:]
    list_courses = [i.text for i in soup_courses]
    list_description = [desc.text for desc in soup_description]

    return [
        Course(
            name=list_courses[i],
            short_description=list_description[i],
            course_type=course_type) for i, course in enumerate(list_courses)
    ]


def get_all_courses() -> list[Course]:
    print("start")
    page = requests.get(BASE_HOST).content
    main_page = BeautifulSoup(page, "html.parser")
    soup_page = main_page.select_one("#part-time")
    part_time = parse_single_course(soup_page, CourseType.PART_TIME)
    full_time = parse_single_course(
        main_page.select_one("#full-time"), CourseType.FULL_TIME
    )
    return [*part_time, *full_time]


if __name__ == "__main__":
    print(get_all_courses())
