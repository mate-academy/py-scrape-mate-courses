from dataclasses import dataclass
from enum import Enum
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules_count: int
    topics_count: int
    duration: Optional[str] = None


def initialize_chrome() -> Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    driver = Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(5)
    return driver


def get_course_detail_info(course_url: str) -> dict:
    course_detail_url = urljoin(URL, course_url) + "#course-program"
    page = requests.get(course_detail_url)
    soup = BeautifulSoup(page.content, "html.parser")
    course_duration = soup.select_one(
        ".CourseModulesHeading_courseDuration__f_c3H p"
    )
    course_info = dict(
        modules_count=int(soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP p"
        ).text.split()[0]),
        topics_count=int(soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR p"
        ).text.split()[0]),
        duration=course_duration.text if course_duration else None
    )
    return course_info


def parse_single_course(course_soup: Tag, course_type: CourseType) -> Course:
    additional_info = get_course_detail_info(
        course_soup.select_one("a")["href"]
    )
    return Course(
        name=course_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=course_soup.select_one(
            ".CourseCard_courseDescription__Unsqj"
        ).text,
        course_type=course_type,
        modules_count=additional_info["modules_count"],
        topics_count=additional_info["topics_count"],
        duration=additional_info["duration"]
    )


def get_all_courses() -> list[Course]:
    driver = initialize_chrome()
    driver.get(URL)
    element = driver.find_element(By.ID, "part-time")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.close()
    full_time_soup = soup.select(
        "[id=full-time] .CourseCard_cardContainer__7_4lK"
    )
    part_time_soup = soup.select(
        "[id=part-time] .CourseCard_cardContainer__7_4lK"
    )
    full_time_courses = [
        parse_single_course(course_soup, CourseType.FULL_TIME)
        for course_soup in full_time_soup
    ]
    part_time_courses = [
        parse_single_course(course_soup, CourseType.PART_TIME)
        for course_soup in part_time_soup
    ]
    return full_time_courses + part_time_courses


if __name__ == "__main__":
    print(get_all_courses())
