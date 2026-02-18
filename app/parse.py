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
    """Fetches course names and URLs from the footer."""
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "lxml")

    course_links = soup.select("ul.FooterLinks_navList__iWcAG > a")

    list_of_courses = [
        (link.text.strip(), link["href"])
        for link in course_links
        if link["href"].startswith("/courses")
    ]

    if list_of_courses:
        list_of_courses.pop()

    return list_of_courses


def parse_course_page(url: str, name: str) -> Course:
    """Extracts detailed information from an individual course page."""
    full_url = urljoin(BASE_URL, url)
    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, "lxml")

    descr_tag = soup.select_one("p.SalarySection_aboutProfession__C6ftM")
    description = descr_tag.text.strip() if descr_tag else ""

    duration = "N/A"
    label_cell = soup.find("div", string="Тривалість")
    if label_cell:
        dur_vals = [
            "".join(filter(str.isdigit, div.text))
            for div in label_cell.find_next_siblings("div")
        ]
        if len(dur_vals) >= 2:
            duration = f"{dur_vals[0]}/{dur_vals[1]} month"

    modules = soup.select("div.CourseModulesList_moduleListItem__b8AY9")
    amount_of_modules = len(modules)
    total_topics = 0

    for module in modules:
        topic_tag = module.select_one("p.CourseModulesList_topicsCount__H_fv3")
        if topic_tag:
            count_digits = "".join(filter(str.isdigit, topic_tag.text))
            total_topics += int(count_digits) if count_digits else 0

    return Course(
        name=name,
        short_description=description,
        duration=duration,
        amount_of_modules=amount_of_modules,
        amount_of_topics=total_topics,
    )


def get_all_courses() -> list[Course]:
    """Orchestrates the scraping of all found courses."""
    course_list = retrieve_list_of_courses()
    return [parse_course_page(url, name) for name, url in course_list]


if __name__ == "__main__":
    all_courses = get_all_courses()
    for course in all_courses:
        print(
            f"{course.name}: {course.duration}, "
            f"{course.amount_of_topics} topics"
        )
