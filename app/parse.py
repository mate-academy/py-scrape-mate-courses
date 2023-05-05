from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(
        course_soup: BeautifulSoup,
        course_type: CourseType
) -> Course:
    course = Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=(
            course_soup.select_one(
                "p", {"class": "typography_"}, partial=True).text
        ),
        course_type=course_type
    )
    print(course)

    return course


def get_all_courses() -> list[Course]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    service = Service("/usr/lib/chromium-browser/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(BASE_URL)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    courses_list = []

    for course_type in CourseType:
        section = soup.find("div", {"id": course_type.value})
        courses = section.findAll(
            "section", {"class": "CourseCard_cardContainer__7_4lK"}
        )

        for course in courses:
            courses_list.append(parse_single_course(course, course_type))

    return courses_list


if __name__ == "__main__":
    get_all_courses()
