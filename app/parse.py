from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    modules: int
    topics: int
    course_type: CourseType


def parse_single_course(
        soup: BeautifulSoup,
        course_type: str
) -> Course:
    detail_page = requests.get(
        URL + soup.select_one("a.CourseCard_button__HTQvE")["href"]
    ).content
    detail_soup = BeautifulSoup(detail_page, "html.parser")

    if course_type == "full-time":
        return Course(
            name=" ".join(soup.select_one(
                ".typography_landingH3__vTjok"
            ).text.split()[1:]),
            short_description=soup.select_one(
                ".CourseCard_courseDescription__Unsqj"
            ).text,
            modules=int(detail_soup.select_one(
                ".CourseModulesHeading_modulesNumber__GNdFP > p"
            ).text.split()[0]),
            topics=int(detail_soup.select_one(
                ".CourseModulesHeading_topicsNumber__PXMnR > p"
            ).text.split()[0]),
            course_type=CourseType.FULL_TIME,
        )
    if course_type == "part-time":
        return Course(
            name=" ".join(soup.select_one(
                ".typography_landingH3__vTjok"
            ).text.split()[1:-1]),
            short_description=soup.select_one(
                ".CourseCard_courseDescription__Unsqj"
            ).text,
            modules=int(detail_soup.select_one(
                ".CourseModulesHeading_modulesNumber__GNdFP > p"
            ).text.split()[0]),
            topics=int(detail_soup.select_one(
                ".CourseModulesHeading_topicsNumber__PXMnR > p"
            ).text.split()[0]),
            course_type=CourseType.PART_TIME,
        )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_courses = soup.select(
        "#full-time .CourseCard_cardContainer__7_4lK"
    )
    part_time_courses = soup.select(
        "#part-time .CourseCard_cardContainer__7_4lK"
    )

    courses = [
        parse_single_course(course, "full-time")
        for course in full_time_courses
    ]
    courses.extend(
        [
            parse_single_course(course, "part-time")
            for course in part_time_courses
        ]
    )

    return courses
