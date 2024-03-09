from urllib.parse import urljoin

import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, ResultSet, Tag


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: str
    topics: str
    duration: str


URL = "https://mate.academy/"


def get_detail_page(endpoint: str) -> BeautifulSoup:
    detail_url = urljoin(URL, endpoint)
    page = requests.get(detail_url).content
    soup = BeautifulSoup(page, "html.parser")
    return soup


def get_page_course() -> ResultSet[Tag]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    return soup.select(".ProfessionCard_cardWrapper__JQBNJ")


def select_part_time_link(course: Tag) -> BeautifulSoup:
    get_part_time = course.select_one(
        ".Button_large__rIMVg[data-qa=parttime-course-more-details-button]"
    ).get("href")
    return get_detail_page(get_part_time)


def select_full_time_link(course: Tag) -> BeautifulSoup:
    get_full_time = course.select_one(
        ".Button_large__rIMVg[data-qa=fulltime-course-more-details-button]"
    ).get("href")
    return get_detail_page(get_full_time)


def get_course(course: Tag, detail_page: BeautifulSoup, time: str) -> Course:
    course_time = (
        CourseType.FULL_TIME if time == "full" else CourseType.PART_TIME
    )
    check = Course(
        name=course.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course.select_one("p.mb-32").text,
        course_type=course_time,
        modules=detail_page.select_one(
            "div.CourseModulesHeading_modulesNumber__UrnUh "
            "> p.CourseModulesHeading_text__bBEaP"
        ).text,
        topics=detail_page.select_one(
            "div.CourseModulesHeading_topicsNumber__5IA8Z "
            "> p.CourseModulesHeading_text__bBEaP"
        ).text,
        duration=detail_page.select_one(
            "div.CourseModulesHeading_courseDuration__qu2Lx "
            "> p.CourseModulesHeading_text__bBEaP"
        ).text
    )
    return check


def get_all_courses() -> list[Course]:
    courses = get_page_course()
    all_course = []
    for course in courses:
        if len(course.select(".Button_large__rIMVg")) > 1:
            all_course.append(
                get_course(
                    course,
                    select_part_time_link(course),
                    "part"
                )
            )
            all_course.append(
                get_course(
                    course,
                    select_full_time_link(course),
                    "full")
            )
        else:
            all_course.append(
                get_course(
                    course,
                    select_part_time_link(course),
                    "part")
            )

    return all_course
