from dataclasses import dataclass
from enum import Enum
from selenium import webdriver

from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"

driver_path = "/usr/local/bin/chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_execuable = webdriver.ChromeService(executable_path=driver_path)
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=chrome_execuable, options=chrome_options)

driver.get(BASE_URL)

html_code = driver.page_source

driver.quit()


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_course_type(soup: BeautifulSoup) -> CourseType:
    course_types = soup.select_one("div > a:last-child")
    course_link = course_types.get("href")
    if "parttime" in course_link:
        return CourseType.PART_TIME
    return CourseType.FULL_TIME


def get_description(soup: BeautifulSoup) -> str:
    description = soup.select_one("p.typography_landingMainText__Ux18x.mb-32")
    if description is None:
        return ""
    return description.text


def parse_single_course(soup: BeautifulSoup) -> Course:
    return Course(
        name=soup.select_one("h3").text,
        short_description=get_description(soup),
        course_type=get_course_type(soup)

    )


def get_all_courses() -> list[Course]:
    soup = BeautifulSoup(html_code, "html.parser")
    courses_soup = soup.select(".ProfessionCard_cardWrapper__DnW_d")
    return [parse_single_course(courses) for courses in courses_soup]
