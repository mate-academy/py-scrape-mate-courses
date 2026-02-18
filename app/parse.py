from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    amount_of_modules: int
    amount_of_topics: int


def retrieve_list_of_courses() -> list[tuple[str, str]]:
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "lxml")

    list_tag = soup.select("ul.FooterLinks_navList__iWcAG > a")
    list_of_courses = [
        (course.text.strip(), course["href"])
        for course in list_tag
        if course["href"].startswith("/courses")
    ]
    list_of_courses.pop()

    return list_of_courses


def parse_course_page(url: str, name: str) -> Course:
    link = urljoin(BASE_URL, url)
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "lxml")

    descr = soup.select_one(
        "p.SalarySection_aboutProfession__C6ftM"
    ).text
    label_cell = soup.find("div", string="Тривалість")
    durations = [
        div.get_text(strip=True)
        for div in label_cell.find_next_siblings("div")
    ]
    duration = f"{durations[0][0]}/{durations[1][0]} month"
    modules = soup.select("div.CourseModulesList_moduleListItem__b8AY9")
    amount_of_modules = len(modules)

    total_topics = 0
    for module in modules:
        topic_tag = module.select_one("p.CourseModulesList_topicsCount__H_fv3")
        if topic_tag:
            count_text = "".join(filter(str.isdigit, topic_tag.get_text()))
            if count_text:
                total_topics += int(count_text)

    return Course(
        name=name,
        short_description=descr,
        duration=duration,
        amount_of_modules=amount_of_modules,
        amount_of_topics=total_topics,
    )


def get_all_courses() -> list[Course]:
    courses = retrieve_list_of_courses()
    all_course_data = []

    for link in courses:
        name, url = link
        course_info = parse_course_page(url, name)
        all_course_data.append(course_info)

    return all_course_data


if __name__ == "__main__":
    get_all_courses()
