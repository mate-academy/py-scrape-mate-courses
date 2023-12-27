import csv
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

URL = "https://mate.academy"

class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_detail_page(course_url):
    page = requests.get(course_url).content
    soup = BeautifulSoup(page, "html.parser")
    description = soup.select_one(".AboutProfessionSection_secondaryBlock__7F__1 .typography_landingTextMain__Rc8BD")
    for info in description:
        short_description = info.text
    return short_description


def parse_single_coursers(course_soup, course_type):
    courses = course_soup.select(".DropdownCoursesList_coursesListItem__5fXRO")
    parsed_courses = []
    for course in courses:
        course_title = course.select_one(".Button_transparentLight__JIwOr")["title"]
        course_link = course.select_one(".Button_transparentLight__JIwOr").get("href")
        course_url = f"{URL}{course_link}"
        short_description = get_detail_page(course_url)

        parsed_courses.append(Course(name=course_title, short_description=short_description, course_type=course_type))
    return parsed_courses


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_full_time = soup.select(".DropdownCoursesList_coursesList__xjALB")[0]
    courses_part_time = soup.select(".DropdownCoursesList_coursesList__xjALB")[1]

    full_time_courses = parse_single_coursers(courses_full_time, CourseType.FULL_TIME)
    part_time_courses = parse_single_coursers(courses_part_time, CourseType.PART_TIME)

    all_courses = full_time_courses + part_time_courses
    return all_courses


def write_to_csv(courses):
    with open('courses_info.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Short Description", "Course Type"])

        for course in courses:
            writer.writerow([course.name, course.short_description, course.course_type.value])


if __name__ == "__main__":
    courses = get_all_courses()
    write_to_csv(courses)
