from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

HOME_URL = "https://mate.academy"


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
    month_duration: str


def get_detail_page(course_soup: BeautifulSoup) -> BeautifulSoup:
    detail_url = course_soup.select_one(".mb-16")["href"]
    page = requests.get(HOME_URL + detail_url).content
    detail_course_soup = BeautifulSoup(page, "html.parser")
    return detail_course_soup


def parse_singe_course(course_soup: BeautifulSoup) -> Course:
    detail_soup = get_detail_page(course_soup)
    month_duration = detail_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H"
    )
    if month_duration:
        month_duration = month_duration.text.split()[0]
    else:
        month_duration = "unlimited"
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=CourseType(course_soup.parent.parent["id"]),
        modules=int(
            detail_soup.select_one(
                ".CourseModulesHeading_modulesNumber__GNdFP"
            ).text.split()[0]
        ),
        topics=int(
            detail_soup.select_one(
                ".CourseModulesHeading_topicsNumber__PXMnR"
            ).text.split()[0]
        ),
        month_duration=month_duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    return [parse_singe_course(course_soup) for course_soup in courses]


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
