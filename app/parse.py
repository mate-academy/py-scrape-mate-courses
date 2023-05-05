from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin

import requests as requests

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_of_modules: int
    num_of_topics: int
    duration: str


def parse_details_course(link: str) -> tuple:
    url = urljoin(BASE_URL, link)
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html.parser")

    num_of_modules = soup.select_one(
        "div.CourseModulesHeading_modulesNumber__GNdFP > p"
    ).text
    num_of_modules = int(num_of_modules.split()[0])

    num_of_topics = soup.select_one(
        "div.CourseModulesHeading_topicsNumber__PXMnR > p"
    ).text
    num_of_topics = int(num_of_topics.split()[0])

    duration = soup.select_one(
        "div.CourseModulesHeading_courseDuration__f_c3H > p"
    )
    duration = duration.text if duration else None

    return num_of_modules, num_of_topics, duration


def parse_course(course: Tag) -> Course:
    title = course.find("span", {"class": "typography_landingH3__vTjok"}).text
    title = " ".join(title.split()[1:])
    description = course.select_one(
        ".CourseCard_courseDescription__Unsqj"
    ).text
    course_type = (
        CourseType.FULL_TIME
        if not title.endswith("Вечірній")
        else CourseType.PART_TIME
    )
    link = course.select_one("div.CourseCard_flexContainer__dJk4p a[href]")[
        "href"
    ]

    details = parse_details_course(link)
    print(
        f"name: {title}",
        f"short_description: {description}",
        f"course_type: {course_type}",
        f"modules: {details[0]}",
        f"topics: {details[1]}",
        f"duration: {details[2]}",
    )

    return Course(
        name=title,
        short_description=description,
        course_type=course_type,
        num_of_modules=details[0],
        num_of_topics=details[1],
        duration=details[2],
    )


def get_all_courses() -> list[Course]:
    service = Service("/usr/local/bin/chromedriver")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(BASE_URL)
    source = BeautifulSoup(driver.page_source, "html.parser")
    courses = source.select(".CourseCard_cardContainer__7_4lK")
    driver.quit()

    return [parse_course(course) for course in courses]
