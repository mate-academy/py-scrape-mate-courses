from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup, Tag

PAGE_URL = "https://mate.academy/ru"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"

    def __repr__(self) -> str:
        return f"{self.value}"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_soup: Tag) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text
    return Course(
        name=name,
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=CourseType.PART_TIME if name.split()[-1] == "Вечерний" else CourseType.FULL_TIME
    )


def get_all_courses() -> list[Course]:
    page = requests.get(PAGE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in courses]


def main() -> None:
    print(get_all_courses())


if __name__ == "__main__":
    main()
