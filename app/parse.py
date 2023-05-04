from pprint import pprint
import time
import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_all_courses() -> list[Course]:
    service = Service("/usr/local/bin/chromedriver")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)
    # wait.until(
    #     EC.presence_of_element_located(
    #         (By.CLASS_NAME, "CourseCard_cardContainer__7_4lK")
    #     )
    # )

    soup = BeautifulSoup(driver.page_source, "html.parser")
    courses = []
    for course_elem in soup.find_all(class_="CourseCard_cardContainer__7_4lK"):
        name_elem = course_elem.find(class_="typography_landingH3__vTjok")
        name = name_elem.text.strip() if name_elem else ""
        short_description_elem = course_elem.find(
            class_="typography_landingMainText__Ux18x "
                   "CourseCard_courseDescription__Unsqj"
        )
        short_description = short_description_elem.text.strip()
        course = Course(
            name=name,
            short_description=short_description,
            course_type=(
                CourseType.PART_TIME if "Вечірній" in name
                else CourseType.FULL_TIME
            )
        )
        courses.append(course)

    driver.quit()

    return courses


if __name__ == "__main__":
    pprint(get_all_courses())
