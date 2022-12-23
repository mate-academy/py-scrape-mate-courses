from dataclasses import dataclass
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


BASE_URL = "https://mate.academy"


def parse_single_type_courses(
        courses_soup: BeautifulSoup,
        course_type: str
) -> [Course]:
    courses = []
    for item_soup in courses_soup:
        course = Course(
            name=item_soup.select("span.typography_landingH3__vTjok")[0].text,
            short_description=item_soup.select(
                "p.typography_landingP1__N9PXd"
            )[0].text,
            course_type=course_type
        )
        courses.append(course)
    return courses


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    full_time_soup = soup.select("#full-time section")
    part_time_soup = soup.select("#part-time section")
    full_time_courses = parse_single_type_courses(
        full_time_soup,
        CourseType.FULL_TIME
    )
    part_time_courses = parse_single_type_courses(
        part_time_soup,
        CourseType.PART_TIME
    )
    all_mate_courses = full_time_courses + part_time_courses
    return all_mate_courses


if __name__ == "__main__":
    get_all_courses()
