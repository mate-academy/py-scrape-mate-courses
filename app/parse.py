from dataclasses import dataclass
from enum import Enum
from pprint import pprint
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    topics: int
    duration: int


def get_detail_course_info(url: str) -> list:
    page = requests.get(urljoin(BASE_URL, url)).content
    soup = BeautifulSoup(page, "html.parser")
    soup_course_info = soup.find(
        "div", "CourseModulesHeading_headingGrid__ynoxV"
    )

    return [int(p.text.split()[0]) for p in soup_course_info.find_all("p")]


def get_single_course(course_soup: BeautifulSoup) -> list[Course]:
    course = []

    name = course_soup.select_one("a.typography_landingH3__vTjok").text
    short_description = course_soup.select_one(
        "p.typography_landingTextMain__Rc8BD.mb-32"
    ).text
    course_types = course_soup.select(".ButtonBody_buttonText__FMZEg")
    modules, topics, duration = get_detail_course_info(
        course_soup.find("a")["href"]
    )

    list_type_names = [name_type.text for name_type in course_types]

    if "Власний темп" in list_type_names:
        course.append(
            Course(
                name=name,
                short_description=short_description,
                course_type=CourseType.PART_TIME,
                modules=modules,
                topics=topics,
                duration=duration,
            )
        )
    if "Повний день" in list_type_names:
        course.append(
            Course(
                name=name,
                short_description=short_description,
                course_type=CourseType.FULL_TIME,
                modules=modules,
                topics=topics,
                duration=duration,
            )
        )
    return course


def get_all_courses() -> list[Course]:
    all_courses = []
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses.extend(
        [course for soup in courses for course in get_single_course(soup)]
    )

    return all_courses


if __name__ == "__main__":
    pprint(get_all_courses())
