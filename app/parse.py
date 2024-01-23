import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, ResultSet, Tag

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


class MateCourseParser:
    def __init__(self) -> None:
        self.base_url = BASE_URL

    def get_page(self) -> bytes:
        return requests.get(self.base_url).content

    def get_page_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.get_page(), "html.parser")

    def get_all_courses_soup(self) -> ResultSet[Tag]:
        return (
            self.get_page_soup().select(".ProfessionCard_cardWrapper__JQBNJ")
        )

    def get_mate_courses(self) -> list[Course]:
        courses_soup = self.get_all_courses_soup()
        courses_list = []

        for course in courses_soup:
            course_name = course.a.string
            short_description = (
                course.select_one(
                    ".typography_landingTextMain__Rc8BD.mb-32"
                ).get_text()
            )
            course_types = course.find_all(
                "span", class_="ButtonBody_buttonText__FMZEg"
            )

            for course_type in course_types:
                course_type_text = course_type.get_text()
                course_type_enum = (
                    CourseType.FULL_TIME
                    if course_type_text == "Повний день"
                    else CourseType.PART_TIME
                )

                courses_list.append(Course(
                    course_name,
                    short_description,
                    course_type_enum
                ))

        return courses_list


def get_all_courses() -> list[Course]:
    parser = MateCourseParser()
    return parser.get_mate_courses()


if __name__ == "__main__":
    get_all_courses()
