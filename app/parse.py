from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: str
    topic: str
    duration: str


def get_detail_course(course_soup: BeautifulSoup) -> BeautifulSoup:
    detail_page_url = course_soup.select_one("a")["href"][1:]
    page = requests.get(BASE_URL + detail_page_url).content
    soup = BeautifulSoup(page, "html.parser")

    return soup


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    name = course_soup.select_one(".typography_landingH3__vTjok").text.strip("Курс")[1:]
    short_description = course_soup.select_one(".CourseCard_flexContainer__dJk4p").text.strip("Детальніше")
    course_type = (
        CourseType.PART_TIME if "Вечірній" in name else CourseType.FULL_TIME
    )
    print(course_type, name)
    detail_page = get_detail_course(course_soup)
    modules = detail_page.select_one(".CourseModulesHeading_modulesNumber__GNdFP").text
    topic = detail_page.select_one(".CourseModulesHeading_topicsNumber__PXMnR").text
    duration = (
        str(
            detail_page.select_one(
                ".CourseModulesHeading_courseDuration__f_c3H > p.CourseModulesHeading_text__EdrEk"
            ).text
        )
        if course_type == CourseType.FULL_TIME
        else "Навчайся у власному графіку"
    )

    return Course(name, short_description, course_type, modules, topic, duration)


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


if __name__ == "__main__":
    print(get_all_courses())
