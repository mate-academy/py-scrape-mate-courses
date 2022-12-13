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
    course_type: CourseType
    modules: int
    topics: int
    duration: int


def get_detail_information(link: str) -> tuple[str | int]:
    url = URL + link[1:]

    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")

    information = soup.select_one(".CourseModulesHeading_headingGrid__50qAP")

    modules = information.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text
    topics = information.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text

    try:
        duration = information.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H > p"
        ).text
    except AttributeError:
        duration = None

    return (int(modules.split()[0]), int(topics.split()[0]), duration)


def get_course(soup: BeautifulSoup) -> Course:
    name = soup.select_one("a.mb-16").text
    short_description = soup.select_one("p").text
    detail_information_link = soup.select_one("a")["href"]

    modules, topics, duration = get_detail_information(detail_information_link)

    if "вечірній" in name.lower():
        course_type = CourseType.PART_TIME
    else:
        course_type = CourseType.FULL_TIME

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type,
        modules=modules,
        topics=topics,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = []

    all_courses = soup.select(".large-6")[:2]

    for i in range(len(all_courses)):
        for course_info in all_courses[i].select(
            ".CourseCard_cardContainer__7_4lK"
        ):
            courses.append(get_course(course_info))

    return courses


def main() -> list[Course]:
    return get_all_courses()


if __name__ == "__main__":
    main()
