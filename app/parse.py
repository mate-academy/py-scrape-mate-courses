from pprint import pprint
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum

HOME_URL = "http://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType


def parse_single_course(courses_soup: BeautifulSoup) -> Course:
    course_dict = dict(
        name=courses_soup.select_one(
            ".typography_landingH3__vTjok").text.split()[-1],
        short_description=courses_soup.select_one(
            ".CourseCard_flexContainer__dJk4p").text,
    )
    if "Вечірній" in course_dict["name"]:
        course_dict["name"] = courses_soup.select_one(
            ".typography_landingH3__vTjok").text.split()[-2]
        course_dict["type"] = CourseType.PART_TIME.value
    else:
        course_dict["type"] = CourseType.FULL_TIME.value
    return Course(**course_dict)


def get_cards_courses():
    page = requests.get(HOME_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return courses


def get_all_courses() -> list[Course]:
    return [parse_single_course(courses_soup) for courses_soup in
            get_cards_courses()]


# optional task
def get_link_detail_single_course_info(courses_soup: BeautifulSoup):
    link = courses_soup.select_one("a").get("href")
    return link


def get_all_detail_course_links() -> list:
    return [urljoin(HOME_URL, get_link_detail_single_course_info(courses_soup))
            for courses_soup in get_cards_courses()]


def get_detail_single_course(url: str):
    detail_page = requests.get(url).content
    soup_detail = BeautifulSoup(detail_page, "html.parser")
    target_option_info = soup_detail.select(
        ".CourseModulesHeading_headingGrid__50qAP")
    return target_option_info


def get_model_topic_duration(detail_page: BeautifulSoup):
    model_numtopic_duration = dict(
        model=detail_page.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP").get_text().split()[
            0],
        numtopic=detail_page.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR").get_text().split()[0],
    )

    try:
        model_numtopic_duration["duration"] = detail_page.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H").get_text().split()[
            0]
    except AttributeError:
        pass
    return model_numtopic_duration


def get_target_option_info_for_courses(links: list):
    detail_target = [get_detail_single_course(link) for link in links]
    result = []
    for target_option in detail_target:
        for value in target_option:
            result.append(get_model_topic_duration(value))

    return result


if __name__ == '__main__':
    pprint(get_all_courses())
