from selenium import webdriver
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


url = "https://mate.academy"
driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")


def get_courses(course_type: Enum) -> list[Course]:
    courses_list = []
    courses = soup.find("div", {"id": course_type.value})
    courses = courses.find_all(
        "section", {"class": "CourseCard_cardContainer__7_4lK"}
    )
    for course in courses:
        title = course.find(
            "span", {"class": "typography_landingH3__vTjok"}
        ).text
        description = course.find(
            "p",
            {
                "class": "typography_landingMainText__Ux18x "
                "CourseCard_courseDescription__Unsqj"
            },
        ).text
        course = Course(
            name=title, short_description=description, course_type=course_type
        )
        courses_list.append(course)
    return courses_list


def get_all_courses() -> list[Course]:
    all_courses = []
    all_courses.extend(get_courses(CourseType.FULL_TIME))
    all_courses.extend(get_courses(CourseType.PART_TIME))
    return all_courses


courses = get_all_courses()
for course in courses:
    print(f"Title: {course.name}\nDescription: {course.short_description}\n")

driver.quit()
