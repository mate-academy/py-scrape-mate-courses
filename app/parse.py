from dataclasses import dataclass, fields
from enum import Enum

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


COURSE_FIELDS = [field.name for field in fields(Course)]


def get_course_type_for_course(course_soup: BeautifulSoup) -> list[CourseType]:
    course_types_html = (
        course_soup
        .find("div", class_="ProfessionCard_buttons__a0o60")
        .find_all("span", class_="ButtonBody_buttonText__FMZEg")
    )

    course_type_texts = [
        course_type.get_text()
        for course_type in course_types_html
    ]
    course_types = []
    for text in course_type_texts:
        if text == "Flex":
            course_types.append(CourseType.PART_TIME)
        else:
            course_types.append(CourseType.FULL_TIME)
    return course_types


def parse_single_course(
        course_soup: BeautifulSoup,
        course_types: [CourseType]
) -> list[Course] | Course:
    course_info = []
    for course_type in course_types:
        course = Course(
            name=course_soup.select_one(".ProfessionCard_title__Zq5ZY").text,
            short_description=course_soup.find(
                "p",
                class_="typography_landingTextMain__Rc8BD mb-32"
            ).get_text(strip=True),
            course_type=course_type
        )
        course_info.append(course)
    return course_info


def get_all_courses() -> list[Course]:
    page = requests.get("https://mate.academy/en").content
    soup = (
        BeautifulSoup(page, "html.parser")
        .select(".ProfessionCard_cardWrapper__JQBNJ")
    )
    list_courses = []
    for soup_info in soup:
        course_types = get_course_type_for_course(soup_info)
        course = parse_single_course(soup_info, course_types)
        list_courses.extend(course)

    return list_courses


if __name__ == "__main__":
    get_all_courses()
