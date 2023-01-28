import time
from dataclasses import dataclass
from enum import Enum

from bs4 import BeautifulSoup
import fake_useragent
import requests

BASE_URL = "https://mate.academy/"

headers = {"User-Agent": fake_useragent.UserAgent().random}


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


def pars_single_course(section) -> tuple:
    return (
        section.select_one("a")["href"],
        section.select_one("a").text,
        section.select_one("p").text,
    )


def detailed_course_data(course_url: str) -> list:
    page = requests.get(BASE_URL + course_url, headers=headers).content
    soup = BeautifulSoup(page, "lxml")

    div = soup.find_all(
        "p",
        attrs={"class": "typography_landingP2__KdC5Q CourseModulesHeading_text__EdrEk"},
    )

    return [p_tag.text for p_tag in div]


def course_list_generator(soup, course_type) -> list[Course]:
    courses = []

    for section in soup:
        course_url, course_name, course_description = pars_single_course(section)
        course_data = detailed_course_data(course_url)

        courses.append(
            Course(
                name=course_name,
                short_description=course_description,
                course_type=course_type,
                modules=course_data[0],
                topics=course_data[1],
                duration=course_data[2] if len(course_data) == 3 else "Невідома",
            )
        )

    return courses


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL, headers=headers).content
    soup = BeautifulSoup(page, "lxml")

    full_time = soup.select("#full-time section")
    part_time = soup.select("#part-time section")

    full_time_list = course_list_generator(full_time, CourseType.FULL_TIME)
    part_time_list = course_list_generator(part_time, CourseType.PART_TIME)
    full_time_list.extend(part_time_list)

    return full_time_list


if __name__ == "__main__":
    start = time.perf_counter()
    all_courses = get_all_courses()
    end = time.perf_counter()

    for course in all_courses:
        print(course)

    print("\n Elapsed:", end - start)
