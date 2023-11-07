from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, Tag
import requests

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course_with_both_course_type(soup: Tag) -> list[Course]:
    name = soup.select_one(".mb-12").text
    short_description = soup.select_one(".mb-32").text
    course_type_elements = soup.select("a[data-qa]")

    course_type = ""
    courses = []
    for element in course_type_elements:
        course_type_text = element["data-qa"]

        if course_type_text.__contains__("fulltime"):
            course_type = CourseType.FULL_TIME
        elif course_type_text.__contains__("parttime"):
            course_type = CourseType.PART_TIME

        course = Course(
            name=name,
            short_description=short_description,
            course_type=course_type
        )
        courses.append(course)

    return courses


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")
    course_cards = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course_card in course_cards:

        courses = parse_single_course_with_both_course_type(course_card)
        all_courses.extend(courses)

    return all_courses


if __name__ == "__main__":
    get_all_courses()
