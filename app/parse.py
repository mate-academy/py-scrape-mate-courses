import csv
from dataclasses import dataclass, fields, astuple
from enum import Enum

import bs4.element
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: str
    num_of_modules: int
    num_of_topics: int
    duration: str


class CourseParser:
    def __init__(self, course_type: CourseType) -> None:
        self.course_type = course_type

    def parse_course(self, course_element: bs4.element.Tag) -> Course:
        name_element = course_element.select_one(
            "a > span.typography_landingH3__vTjok"
        )
        description_element = course_element.select_one("div > p")
        details_url = course_element.select_one("a")["href"][3:]
        details_page = requests.get(BASE_URL + details_url).content
        details_soup = BeautifulSoup(details_page, "html.parser")

        def get_text(selector: str) -> str:
            return details_soup.select_one(selector).get_text(strip=True)

        num_of_modules = int(
            get_text(
                ".CourseModulesHeading_modulesNumber__GNdFP > p"
            ).split()[0]
        )
        num_of_topics = int(
            get_text(
                ".CourseModulesHeading_topicsNumber__PXMnR > p"
            ).split()[0]
        )
        duration = get_text(
            ".CourseModulesHeading_courseDuration__f_c3H > p"
        )

        return Course(
            name=name_element.text,
            short_description=description_element.text,
            course_type=self.course_type.value,
            num_of_modules=num_of_modules,
            num_of_topics=num_of_topics,
            duration=duration
        )


class Parser:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @staticmethod
    def parse_courses(page_soup: BeautifulSoup) -> list[Course]:
        course_containers = {
            CourseType.FULL_TIME: page_soup.select(
                "#full-time > div.cell.large-6.large-offset-1.mb-32 > section"
            ),
            CourseType.PART_TIME: page_soup.select(
                "#part-time > div.cell.large-6.large-offset-1 > section"
            )
        }
        all_courses = []
        for course_type, course_elements in course_containers.items():
            course_parser = CourseParser(course_type)
            for course_element in course_elements:
                course = course_parser.parse_course(course_element)
                all_courses.append(course)
        return all_courses

    def get_all_courses(self) -> None:
        page = requests.get(self.base_url).content
        soup = BeautifulSoup(page, "html.parser")
        courses = self.parse_courses(page_soup=soup)
        self.write_to_csv(courses, "courses.csv")

    @staticmethod
    def write_to_csv(courses: list[Course], file_name: str) -> None:
        with open(
                file_name,
                "w",
                encoding="utf-8",
                newline=""
        ) as courses_file:
            writer = csv.writer(courses_file)
            writer.writerow([field.name for field in fields(Course)])
            writer.writerows([astuple(course) for course in courses])


if __name__ == "__main__":
    parser = Parser(BASE_URL)
    parser.get_all_courses()
