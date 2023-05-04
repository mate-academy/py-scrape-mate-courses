from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_course(course_soup: Tag, course_type: CourseType) -> Course:
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
    )


def get_all_courses() -> list[Course]:
    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    full_time_soup = soup.select(
        "[id=full-time] .CourseCard_cardContainer__7_4lK"
    )
    part_time_soup = soup.select(
        "[id=part-time] .CourseCard_cardContainer__7_4lK"
    )
    full_time_courses = [
        parse_course(course_soup, CourseType.FULL_TIME)
        for course_soup in full_time_soup
    ]
    part_time_courses = [
        parse_course(course_soup, CourseType.PART_TIME)
        for course_soup in part_time_soup
    ]
    return full_time_courses + part_time_courses


if __name__ == "__main__":
    print(get_all_courses())
