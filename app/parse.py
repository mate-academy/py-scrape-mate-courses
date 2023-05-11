from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    topics: int
    modules: int
    duration: str


def parse_single_course(course_soup: Tag) -> Course:
    detail_url = urljoin(BASE_URL, course_soup.select_one("a")["href"])
    detail_page = requests.get(detail_url).content
    detail_soup = BeautifulSoup(detail_page, "html.parser")
    course_name = course_soup.select_one(".typography_landingH3__vTjok").text
    course_description = course_soup.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    num_modules = int(detail_soup.select_one(
        ".CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text.split()[0])
    num_topics = int(detail_soup.select_one(
        ".CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text.split()[0])
    course_duration = detail_soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H > p"
    )
    if course_duration is not None:
        course_duration = f"{course_duration.text.split()[0]} months"
    else:
        course_duration = "Up to you"
    return Course(
        name=course_name,
        short_description=course_description,
        course_type=(CourseType.FULL_TIME,
                     CourseType.PART_TIME)["Вечірній" in course_name],
        modules=num_modules,
        topics=num_topics,
        duration=course_duration
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")
    courses = [parse_single_course(course) for course in courses]
    return courses


if __name__ == "__main__":
    print(get_all_courses())
