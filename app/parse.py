from dataclasses import dataclass
from enum import Enum
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_single_course(section: str, course_type: CourseType) -> Course:
    name = section.select_one(".typography_landingH3__vTjok").text
    short_description = section.select_one(
        ".typography_landingMainText__Ux18x"
    ).text
    return Course(name, short_description, course_type)


def get_all_courses() -> list[Course]:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    # time.sleep(15)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.quit()

    block_ft = soup.find("div", {"id": "full-time"})
    sections1 = block_ft.select(".CourseCard_cardContainer__7_4lK")
    full_time_list = [
        get_single_course(section, CourseType.FULL_TIME)
        for section in sections1
    ]

    block_pt = soup.find("div", {"id": "part-time"})
    sections2 = block_pt.select(".CourseCard_cardContainer__7_4lK")
    part_time_list = [
        get_single_course(section, CourseType.PART_TIME)
        for section in sections2
    ]

    full_time_list.extend(part_time_list)
    return full_time_list


def main() -> None:
    print(get_all_courses())


if __name__ == "__main__":
    main()
