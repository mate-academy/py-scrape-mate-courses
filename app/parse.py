from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, ResultSet, Tag


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
    duration: str


def get_parse_detail_course_page(course_soup: Tag, base_url: str) -> ResultSet[Tag]:
    detail_url = urljoin(base_url, course_soup.select_one("a.mb-16")["href"])
    page = requests.get(detail_url).content
    soup = BeautifulSoup(page, "html.parser")
    return soup.select(".CourseModulesHeading_headingGrid__50qAP")


def parse_single_course(course_soup: Tag, base_url: str) -> Course:
    programma_soup = get_parse_detail_course_page(course_soup, base_url)
    modules = 0
    topics = 0
    duration = ""
    for item in programma_soup:
        modules = int(item.select_one(
            "div.CourseModulesHeading_modulesNumber__GNdFP p"
        ).text.split()[0])
        topics = int(item.select_one(
            "div.CourseModulesHeading_topicsNumber__PXMnR p"
        ).text.split()[0])
        try:
            duration = item.select_one(
                "div.CourseModulesHeading_courseDuration__f_c3H p"
            ).text.split()[0]
        except AttributeError:
            duration = "undefined"
    if len(course_soup.select_one(
            "span.typography_landingH3__vTjok"
    ).text.split()) == 3:
        course_type = CourseType.PART_TIME
    else:
        course_type = CourseType.FULL_TIME
    return Course(
        name=course_soup.select_one(
            "span.typography_landingH3__vTjok"
        ).text.split()[1],
        short_description=course_soup.select_one(
            "p.CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
        modules=modules,
        topics=topics,
        duration=duration,
    )


def get_all_courses() -> [Course]:
    base_url = "https://mate.academy/"
    page = requests.get(base_url).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select("section.CourseCard_cardContainer__7_4lK")
    return [parse_single_course(course, base_url) for course in courses]


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
