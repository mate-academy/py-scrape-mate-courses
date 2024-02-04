import csv
from dataclasses import dataclass, fields, astuple
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


COURSES_FIELDS = [field.name for field in fields(Course)]


@dataclass
class AdditionalInfo:
    name: str
    course_type: str
    modules: int
    topics: int
    duration: str


INFO_FIELDS = [field.name for field in fields(AdditionalInfo)]


def get_content_from_url(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Request failed with status code {response.status_code}")


def get_item_some_course(some_course: BeautifulSoup) -> list:
    name = some_course.select_one("a").get_text(strip=True)
    short_description = some_course.select_one("p:nth-of-type(2)").get_text(
        strip=True
    )
    return [name, short_description]


def create_course(
    course_name: str, short_description: str, course_type: CourseType
) -> Course:
    return Course(
        name=course_name,
        short_description=short_description,
        course_type=course_type,
    )


def get_some_course(
    course_type_one: str, name: str, short_description: str
) -> list[Course]:
    course_list = []
    if course_type_one == "Власний темп":
        course_type = CourseType.PART_TIME
        course_list.append(create_course(name, short_description, course_type))
    elif course_type_one == "Повний день":
        course_type = CourseType.FULL_TIME
        course_list.append(create_course(name, short_description, course_type))

    return course_list


def get_course_type(some_course: BeautifulSoup) -> list:
    course_type_all = [
        span.get_text(strip=True)
        for span in some_course.select(".ProfessionCard_buttons__a0o60 span")
    ]
    return course_type_all


def get_course_href(some_course: BeautifulSoup) -> list:
    href_list = [
        a["href"]
        for a in some_course.select(".ProfessionCard_buttons__a0o60 a")
    ]
    return href_list


def get_additional_info_some_page(url: str) -> list:
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html.parser")
    name = soup.select_one(".grid-container h1").get_text()
    print(name)
    type_course = soup.select_one(
        ".CourseHeroSection_sectionWrapper__yjw_1 p"
    ).get_text(strip=True)
    print(type_course)
    modules = int(
        soup.select_one(".CourseModulesHeading_modulesNumber__GNdFP p")
        .get_text(strip=True)
        .split()[0]
    )
    print(modules)
    topics = int(
        soup.select_one(".CourseModulesHeading_topicsNumber__PXMnR p")
        .get_text(strip=True)
        .split()[0]
    )
    print(topics)
    duration = (
        soup.select_one(".CourseModulesHeading_courseDuration__f_c3H p")
        .get_text(strip=True)
        .replace("місяців", "months")
    )
    print(duration)
    return [name, modules, topics, duration, type_course]


def get_additional_info_all_page(links: list) -> list[AdditionalInfo]:
    res_add_info_list = []
    for link in links:
        url = urljoin(BASE_URL, link)
        (
            name,
            modules,
            topics,
            duration,
            type_course,
        ) = get_additional_info_some_page(url)
        add_info = AdditionalInfo(
            name=name,
            modules=modules,
            topics=topics,
            duration=duration,
            course_type=type_course,
        )
        res_add_info_list.append(add_info)
    return res_add_info_list


def get_all_courses_add_info() -> [Course, list]:
    result_course_list = []
    result_href_list = []
    response = get_content_from_url(BASE_URL)
    soup = BeautifulSoup(response, "html.parser")
    professional_cards = soup.find_all(
        "div", class_="ProfessionCard_cardWrapper__JQBNJ"
    )
    for some_course in professional_cards:
        name, short_description = get_item_some_course(some_course)
        course_type_all = get_course_type(some_course)
        href_list = get_course_href(some_course)

        for course_type_one in course_type_all:
            course_list = get_some_course(
                course_type_one, name, short_description
            )
            result_course_list.extend(course_list)
        result_href_list.extend(href_list)
    return [result_course_list, result_href_list]


# this is an unnecessary helper function,
# because otherwise the tests do not work.
# Everything works great without it
def get_all_courses() -> list[Course]:
    course_list, result_href_list = get_all_courses_add_info()
    return course_list


def write_csv(path: str, items: list, column_headings: list) -> None:
    with open(path, "w", newline="", encoding="utf-8") as file:
        quote_writer = csv.writer(file)
        quote_writer.writerow(column_headings)
        quote_writer.writerows([astuple(quote) for quote in items])


def main() -> None:
    courses, links = get_all_courses()
    write_csv("courses.csv", courses, COURSES_FIELDS)
    print(links)
    add_info_list = get_additional_info_all_page(links)
    write_csv("additional_info.csv", add_info_list, INFO_FIELDS)


if __name__ == "__main__":
    main()
