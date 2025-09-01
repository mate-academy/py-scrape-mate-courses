import csv
from dataclasses import dataclass, fields

import requests
from bs4 import BeautifulSoup, Tag
from requests import RequestException

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_num: int
    topics_num: int


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(page_soup: Tag) -> Course:
    meta_tag = page_soup.find('meta', {'name': 'description'})
    description = meta_tag['content'] if meta_tag else ""

    duration_label = page_soup.find(
        'div',
        class_='c-text-secondary typography_labelSmall__FERSi',
        string='Тривалість'
    )
    duration = ""
    if duration_label:
        parent_div = duration_label.find_parent(
            'div',
            class_='TableFeedView_rowWithButtons__j6_7p'
        )
        duration_value = parent_div.find_next('div', class_='c-text-dark')
        duration = duration_value.get_text()

    topics_num = len(page_soup.select_one(
                'ul.CourseModulesList_modulesList__C86yL'
            ).find_all('li', recursive=False))
    modules_num = len(page_soup.select_one(
                'ul.CourseModulesList_modulesList__C86yL'
            ).find_all('li')) - topics_num

    return Course(
        name=str(page_soup.select_one(".typography_small_headlineXSmall___65od").text),
        short_description=description,
        duration=str(duration),
        modules_num=modules_num,
        topics_num=topics_num,
    )


def get_all_courses() -> list[Course]:
    try:
        page_response = requests.get(BASE_URL)
        page_response.raise_for_status()
        page_content = BeautifulSoup(page_response.content, "html.parser")
    except RequestException as e:
        print(
            f"Warning: Could not fetch courses list from {BASE_URL}: {e}"
        )
        return [Course(name="", short_description="", duration="", modules_num=0, topics_num=0)]

    courses_links = [
        link.get('href') for link in page_content.select(
            'li a[data-qa="dropdown-profession-item"]'
        )
    ]
    courses = []
    print("Parsing courses links:")
    for course_link in courses_links:
        page_course_response = requests.get(BASE_URL + course_link[1:])
        page_course_response.raise_for_status()
        page_course_content = BeautifulSoup(page_course_response.content, "html.parser")

        print(BASE_URL + course_link[1:])
        courses.append(parse_single_course(page_course_content))

    return courses



def write_courses_to_csv(courses: list[Course], output_csv_path: str) -> None:
    with open(output_csv_path, "w", newline="", encoding="utf-16") as f:
        writer = csv.writer(f)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([
            (course.name, course.short_description, course.duration, course.modules_num, course.topics_num,)
            for course in courses
        ])


def main(output_csv_path: str) -> None:
    write_courses_to_csv(get_all_courses(), output_csv_path)


if __name__ == "__main__":
    main("courses.csv")
