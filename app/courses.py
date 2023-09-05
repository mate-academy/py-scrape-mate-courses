from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

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
    num_modules: int
    num_topics: int
    duration_months: int


def parse_course_details(detail_url: str) -> dict:
    detail_page = requests.get(detail_url).content
    detail_soup = BeautifulSoup(detail_page, "html.parser")
    course_details = {
        "num_modules": int(detail_soup.select_one(".CourseModulesHeading_modulesNumber__GNdFP > p").text.split()[0]),
        "num_topics": int(detail_soup.select_one(".CourseModulesHeading_topicsNumber__PXMnR > p").text.split()[0]),
        "duration_months": int(detail_soup.select_one(".CourseModulesHeading_courseDuration__f_c3H > p").text.split()[0]),
    }
    print(course_details)
    return course_details


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    detail_url = urljoin(BASE_URL, course_soup.select_one("sectionCourseCard_cardContainer__7_4lK > a.mb-16")["href"])
    course_detail = parse_course_details(detail_url=detail_url)
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(".typography_landingMainText__Ux18x.CourseCard_courseDescription__Unsqj").text,
        course_type=CourseType.PART_TIME if course_soup.select(".Button_black__kAQvx.CourseCard_button__HTQvE") else CourseType.FULL_TIME,
        num_modules=course_detail.get("num_modules", "Something went wrong with num modules"),
        num_topics=course_detail.get("num_topics", "Something went wrong with num topics"),
        duration_months=course_detail.get("duration_months", "Something went wrong with duration months"),
    )


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select("description")
    return [parse_single_course(course) for course in courses]
