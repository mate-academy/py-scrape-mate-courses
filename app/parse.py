import csv
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
from dataclasses import astuple

from . import course as c
from .course import CourseType as C_type


BASE_MATE_ACADEMY = "https://mate.academy/"


def write_in_cvs_file(
        column_fields: [str],
        data: [c.Course],
        csv_file: str
) -> None:
    with open(csv_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(column_fields)
        writer.writerows([astuple(record) for record in data])


def course_detail_page(course_link: Tag) -> BeautifulSoup:
    """Get course detail page"""
    detail_link = urljoin(BASE_MATE_ACADEMY, course_link["href"])
    page = requests.get(detail_link).content
    page_soup = BeautifulSoup(page, "html.parser")

    return page_soup


def create_courses(course_soup: BeautifulSoup) -> list[c.Course]:
    course = {
        "name": course_soup.select_one(c.NAME).string,
        "short_description": course_soup.select_one(
            c.SHORT_DESCRIPTION
        ).string,
    }

    courses = []
    for course_link in course_soup.select(c.PART_FULL_LINKS):
        course_detail = course_detail_page(course_link)

        courses.append(
            c.Course(
                **course,
                course_type=(
                    C_type.FULL_TIME
                    if "fulltime" in course_link["data-qa"]
                    else C_type.PART_TIME
                ),
                num_modules=int(
                    course_detail.select_one(c.NUM_MODULES).string.split()[0]
                ),
                num_topics=int(
                    course_detail.select_one(c.NUM_TOPICS).string.split()[0]
                ),
                duration=course_detail.select_one(c.DURATION).string,
            )
        )

    return courses


def get_all_courses() -> list[c.Course]:
    page = requests.get(BASE_MATE_ACADEMY).content
    page_soup = BeautifulSoup(page, "html.parser")
    courses = page_soup.select(c.COURSES_CARD)
    result = []
    for course in courses:
        result.extend(create_courses(course))
    return result
