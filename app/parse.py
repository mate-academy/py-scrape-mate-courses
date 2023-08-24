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
    course_type: CourseType
    num_of_modules: int
    num_of_topics: int
    duration: str


class Parser:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = requests.Session()

    def parse_single_course(
            self,
            course_element: bs4.element.Tag,
            course_type: CourseType
    ) -> Course:
        name_element = course_element.select_one(
            "a > span.typography_landingH3__vTjok"
        )
        description_element = course_element.select_one("div > p")
        details_url = course_element.select_one("a")["href"][3:]
        details_page = self.session.get(self.base_url + details_url).content
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
        duration = get_text(".CourseModulesHeading_courseDuration__f_c3H > p")

        return Course(
            name=name_element.text,
            short_description=description_element.text,
            course_type=course_type,
            num_of_modules=num_of_modules,
            num_of_topics=num_of_topics,
            duration=duration
        )

    def parse_courses(self) -> list[Course]:
        page = self.session.get(self.base_url).content
        page_soup = BeautifulSoup(page, "html.parser")
        course_containers = {
            CourseType.FULL_TIME: page_soup.select(
                "#full-time > div.cell.large-6.large-offset-1.mb-32 > section"
            ),
            CourseType.PART_TIME: page_soup.select(
                "#part-time > div.cell.large-6.large-offset-1 > section"
            )
        }
        all_courses = [
            self.parse_single_course(
                course_element,
                course_type
            )
            for course_type, course_elements in course_containers.items()
            for course_element in course_elements
        ]
        return all_courses

    @staticmethod
    def write_to_csv(courses: list[Course], file_name: str) -> None:
        with open(
                file=file_name,
                mode="w",
                encoding="utf-8",
                newline=""
        ) as courses_file:
            writer = csv.writer(courses_file)
            writer.writerow([field.name for field in fields(Course)])
            writer.writerows([astuple(course) for course in courses])


def get_all_courses() -> list[Course]:
    parser = Parser(BASE_URL)
    courses = parser.parse_courses()
    parser.write_to_csv(courses, "courses.csv")
    return courses


if __name__ == "__main__":
    get_all_courses()
