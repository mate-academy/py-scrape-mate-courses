from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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


BASE_URL = "https://mate.academy/"


def get_course_detail_data(url: str) -> tuple:
    page = requests.get(urljoin(BASE_URL, url)).content
    soup = BeautifulSoup(page, "html.parser")

    return (
        soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP p"
        ).text.split()[0],
        soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR p"
        ).text.split()[0],
        soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H p"
        ).text.split()[0],
    )


def get_single_course_full_time(course: BeautifulSoup) -> Course:
    url = course.select_one(".Button_primary__7fH0C")["href"]
    additional_data = get_course_detail_data(url)
    return Course(
        name=course.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course.select(
            ".typography_landingTextMain__Rc8BD"
        )[1].text,
        course_type=CourseType.FULL_TIME,
        modules=additional_data[0],
        topics=additional_data[1],
        duration=additional_data[2],
    )


def get_single_course_part_time(course: BeautifulSoup) -> Course:
    url = course.select_one(".Button_secondary__DNIuD")["href"]
    additional_data = get_course_detail_data(url)
    return Course(
        name=course.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course.select(
            ".typography_landingTextMain__Rc8BD"
        )[1].text,
        course_type=CourseType.PART_TIME,
        modules=additional_data[0],
        topics=additional_data[1],
        duration=additional_data[2],
    )


def get_single_page_courses(page: BeautifulSoup) -> [Course]:
    courses = []

    for course in page.select(".ProfessionCard_cardWrapper__JQBNJ"):
        if course.select_one(".Button_secondary__DNIuD"):
            courses.append(get_single_course_part_time(course))
        if course.select_one(".Button_primary__7fH0C"):
            courses.append(get_single_course_full_time(course))

    return courses


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    return get_single_page_courses(soup)


if __name__ == "__main__":
    get_all_courses()
