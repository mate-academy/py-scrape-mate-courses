from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
import requests


BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    other_parameters: dict


def take_parameters_from_links(course, type) -> dict:
    link = course.select_one("a.mb-16")
    course_page = requests.get(BASE_URL + link.attrs.get("href")).content
    soup = BeautifulSoup(course_page, "html.parser")

    other_params = {
        "modules": soup.select_one(
            "div.CourseModulesHeading_modulesNumber__GNdFP p"
        ).text.split()[0],
        "topics": soup.select_one(
            "div.CourseModulesHeading_topicsNumber__PXMnR p"
        ).text.split()[0],
    }
    if type == CourseType.FULL_TIME:
        other_params["duration"] = soup.select_one(
            "div.CourseModulesHeading_courseDuration__f_c3H p"
        ).text.split()[0]

    return other_params


def get_all_courses() -> list[Course]:

    mate_page = requests.get(BASE_URL).content
    soup = BeautifulSoup(mate_page, "html.parser")
    courses = soup.select(
        ".section_scrollSection__RBDyT .CourseCard_cardContainer__7_4lK"
    )
    result = []

    for course in courses:
        name = course.select_one(".typography_landingH3__vTjok").text
        short_description = course.select_one(
            ".typography_landingP1__N9PXd"
        ).text
        type = CourseType.FULL_TIME

        if name.split()[-1] == "Вечірній":
            type = CourseType.PART_TIME

        other_parameters = take_parameters_from_links(course, type)

        course_obj = Course(
            name=name,
            short_description=short_description,
            type=type,
            other_parameters=other_parameters,
        )
        result.append(course_obj)
    return result
