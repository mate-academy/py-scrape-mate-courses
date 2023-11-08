from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup

HOME_URL = "https://mate.academy/"


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


def get_course_type(soup: BeautifulSoup) -> list[CourseType]:
    all_buttons = soup.select(".ProfessionCard_buttons__a0o60")
    list_of_types = []
    for buttons in all_buttons:
        for course_type in buttons.find_all("a"):
            if "Власний темп" in course_type.text:
                list_of_types.append(CourseType.PART_TIME)
            if "Повний день" in course_type.text:
                list_of_types.append(CourseType.FULL_TIME)

    return list_of_types


def parse_page_of_course(detail_link: str) -> list:
    page = requests.get(HOME_URL + detail_link).content
    beautiful_soup = BeautifulSoup(page, "html.parser")

    modules = beautiful_soup.select_one(".CourseModulesHeading_modulesNumber__GNdFP").text
    topics = beautiful_soup.select_one(".CourseModulesHeading_topicsNumber__PXMnR").text
    duration = beautiful_soup.select_one(".CourseModulesHeading_courseDuration__f_c3H").text

    return [int(modules.split()[0]), int(topics.split()[0]), duration]


def parse_course(soup: BeautifulSoup) -> list[Course]:
    name = soup.select_one(".ProfessionCard_title__Zq5ZY").text
    short_description = soup.select_one(".typography_landingTextMain__Rc8BD.mb-32").text
    detail_link = soup.select_one("a")["href"]
    modules, topics, duration = parse_page_of_course(detail_link)
    courses_list = [
        Course(
            name=name,
            short_description=short_description,
            course_type=course_type,
            modules=modules,
            topics=topics,
            duration=duration
        )
        for course_type in get_course_type(soup)
    ]
    return courses_list


def get_all_courses() -> list[Course]:
    page = requests.get(HOME_URL).content
    beautiful_soup = BeautifulSoup(page, "html.parser")

    courses_soup = beautiful_soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    result = []
    for course in courses_soup:
        result.extend(parse_course(course))

    return result


if __name__ == '__main__':
    for course in get_all_courses():
        print(course)
