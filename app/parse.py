import re
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urljoin

import requests as requests

HOME_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    modules: int
    topics: int
    duration: int


def get_main_info(soup):
    title = soup.select_one(".typography_landingH3__vTjok").text

    info = [
        title,
        soup.select_one(".CourseCard_courseDescription__Unsqj").text,
        CourseType.PART_TIME.value
        if "Вечірній" in title
        else CourseType.FULL_TIME.value
    ]
    return info


def urls(home_soup: BeautifulSoup):
    return [urljoin(HOME_URL, tag['href'])
            for tag in home_soup.find_all("a", {'href': re.compile("courses"), 'class': 'mb-16'})]


def get_extra_info(url: str):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    extra_info = [
        soup.select_one('.CourseModulesHeading_modulesNumber__GNdFP').text.split()[0],
        soup.select_one('.CourseModulesHeading_topicsNumber__PXMnR').text.split()[0]
    ]
    try:
        extra_info.append(soup.select_one('.CourseModulesHeading_courseDuration__f_c3H').text.split()[0])
    except AttributeError:
        extra_info.append('unlimited')
    return extra_info


def get_single_course(**info) -> Course:
    return Course(**info)


def get_all_info() -> list[Course]:
    home_page = requests.get(HOME_URL).content
    home_soup = BeautifulSoup(home_page, "html.parser")

    courses_mi = home_soup.select(".CourseCard_cardContainer__7_4lK")
    external_links = urls(home_soup)

    main_info = [get_main_info(course) for course in courses_mi]
    extra_info = [get_extra_info(link) for link in external_links]

    info = [main_info[i] + extra_info[i] for i in range(len(main_info))]
    info_dict = [
        {'name': el[0],
         'short_description': el[1],
         'type': el[2],
         'modules': el[3],
         'topics': el[4],
         'duration': el[5],
         } for el in info
    ]

    return [get_single_course(**el) for el in info_dict]


if __name__ == '__main__':
    pprint(get_all_info())
