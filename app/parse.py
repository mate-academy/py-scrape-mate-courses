from typing import List

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup, Tag, ResultSet
from dataclasses import dataclass
from enum import Enum

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        name: str,
        description: str,
        course_type: CourseType
) -> Course:
    return Course(
        name=name,
        short_description=description,
        course_type=course_type
    )


def parse_all_courses(full_time_soup: ResultSet[Tag]) -> List[Course]:
    names = [course.select_one(
        ".mb-16 span"
    ).text for course in full_time_soup]
    descriptions = [
        course.select_one(
            ".CourseCard_flexContainer__dJk4p p"
        ).text for course in full_time_soup
    ]

    courses = []
    for name, description in zip(names, descriptions):
        course_type = CourseType.FULL_TIME if len(
            name.split()
        ) < 3 else CourseType.PART_TIME
        course = parse_single_course(name.split()[1], description, course_type)
        courses.append(course)

    return courses


def get_all_parsed_curses(page_soup: BeautifulSoup) -> List[Course]:
    course_soup = page_soup.select("section .CourseCard_cardContainer__7_4lK")
    courses = parse_all_courses(course_soup)
    return courses


def get_all_courses() -> List[Course]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        "/usr/lib/chromium-browser/chromedriver",
        options=chrome_options
    )
    driver.get(HOME_URL)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    courses = get_all_parsed_curses(soup)
    driver.quit()

    return courses


print(get_all_courses())
# import requests
#
# from typing import List
# from bs4 import BeautifulSoup, Tag, ResultSet
# from dataclasses import dataclass
# from enum import Enum
#
# HOME_URL = "https://mate.academy/"
#
#
# class CourseType(Enum):
#     FULL_TIME = "full-time"
#     PART_TIME = "part-time"
#
#
# @dataclass
# class Course:
#     name: str
#     short_description: str
#     course_type: CourseType
#
#
# def parse_single_course(name: str, description: str, course_type: CourseType) -> Course:
#     return Course(name=name, short_description=description, course_type=course_type)
#
#
# def parse_full_time_courses(page_soup: ResultSet[Tag]) -> List[Course]:
#     full_time_soup = page_soup.select("section .CourseCard_cardContainer__7_4lK")
#     names = [course.select_one(".mb-16 span").text for course in full_time_soup]
#     descriptions = [course.select_one(".CourseCard_flexContainer__dJk4p p").text for course in full_time_soup]
#
#     courses = []
#     for name, description in zip(names, descriptions):
#         course_type = CourseType.FULL_TIME
#         course = parse_single_course(name.split()[1], description, course_type)
#         courses.append(course)
#
#     return courses
#
#
# def parse_part_time_courses(page_soup: ResultSet[Tag]) -> List[Course]:
#     # print(page_soup.prettify())
#     description_for_recruitment = page_soup.prettify().split('null,"description":')[1].split(',"')[0]
#     print(description_for_recruitment)
#     part_time_soup = page_soup.select("span.ButtonBody_buttonText__FMZEg")
#     names = [course.text.split()[0] for course in part_time_soup if "Вечірній" in course.text]
#     # descriptions = [course.select_one(".CourseCard_flexContainer__dJk4p p").text for course in full_time_soup]
#
#     courses = []
#     # for name, description in zip(names, descriptions):
#     #     course_type = CourseType.FULL_TIME if len(name.split()) < 3 else CourseType.PART_TIME
#     #     course = parse_single_course(name.split()[1], description, course_type)
#     #     courses.append(course)
#
#     return courses
#
#
# def parse_all_courses(page_soup: ResultSet[Tag]) -> List[Course]:
#     full_time_courses = parse_full_time_courses(page_soup)
#     part_time_courses = parse_part_time_courses(page_soup)
#     return full_time_courses
#
#
# def get_parsed_courses(page_soup: BeautifulSoup) -> List[Course]:
#     courses = parse_all_courses(page_soup)
#     return courses
#
#
# def get_all_courses() -> List[Course]:
#     r = requests.get(HOME_URL).content
#     soup = BeautifulSoup(r, 'html.parser')
#     courses = get_parsed_courses(soup)
#
#     return courses
#
#
# print(get_all_courses())
