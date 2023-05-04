import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DOMAIN_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    topics: int
    duration: str


def parse_course_detail_page(course_soup: BeautifulSoup) -> BeautifulSoup:
    course_page_url = course_soup.select_one("a")["href"]
    page = requests.get(DOMAIN_URL + course_page_url).content
    soup = BeautifulSoup(page, "html.parser")

    return soup


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    course_detail_page = parse_course_detail_page(course_soup)
    name = " ".join(course_soup.select_one("span").text.split()[1:])
    duration_element = course_detail_page.select_one("[class*=courseDuration]")
    duration = (
        duration_element.text
        if duration_element is not None
        else "Your life - your rules)"
    )
    return Course(
        name=name,
        short_description=course_soup.select_one("p").text,
        course_type=(
            CourseType.PART_TIME
            if "Вечірній" in name
            else CourseType.FULL_TIME
        ),
        modules=int(
            course_detail_page.select_one(
                "[class*=modulesNumber]"
            ).text.split()[0]
        ),
        topics=int(
            course_detail_page.select_one(
                "[class*=topicsNumber]"
            ).text.split()[0]
        ),
        duration=duration,
    )


def get_html_page(url: str = DOMAIN_URL) -> str:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    driver.implicitly_wait(2)
    html = driver.page_source

    driver.quit()

    return html


def get_all_courses() -> list[Course]:
    page = get_html_page()
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses]


if __name__ == "__main__":
    print(get_all_courses())
