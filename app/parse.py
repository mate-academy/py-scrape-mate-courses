import csv
import logging
import requests
import sys

from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass, astuple, fields
from enum import Enum
from typing import Self
from urllib.parse import urljoin


BASE_URL = "https://mate.academy/en"
OUTPUT_CSV_PATH = "courses_data.csv"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


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

    @staticmethod
    def get_course_additional_details(course_detail_url: str) -> dict:
        course_detail_page = requests.get(
            urljoin(BASE_URL, course_detail_url)
        ).content
        course_detail_soup = BeautifulSoup(course_detail_page, "html.parser")

        course_additional_details = dict(
            modules=int(course_detail_soup.select_one(
                ".CourseModulesHeading_modulesNumber__GNdFP"
            ).text.split()[0]),
            topics=int(course_detail_soup.select_one(
                ".CourseModulesHeading_topicsNumber__PXMnR"
            ).text.split()[0]),
            duration=course_detail_soup.select_one(
                ".CourseModulesHeading_courseDuration__f_c3H"
            ).text,
        )

        return course_additional_details

    @classmethod
    def get_single_course_full_details(cls, course: Tag) -> Self:
        course_detail_url = course.select_one(".mb-16")["href"]
        course_type_in_url = (
            course.select_one("a.mb-16")["href"].split("-")[-1]
        )

        course_name = course.select_one(".typography_landingH3__vTjok").text
        logging.info(f"Parsing course: {course_name}")

        course_base_details = dict(
            name=course_name,
            short_description=course.select_one(
                "p.CourseCard_courseDescription__Unsqj"
            ).text,
            course_type=(
                CourseType.PART_TIME
                if course_type_in_url == "parttime"
                else CourseType.FULL_TIME
            )
        )
        course_additional_details = cls.get_course_additional_details(
            course_detail_url
        )

        return cls(
            **course_base_details,
            **course_additional_details
        )


def get_all_courses() -> list[Course]:
    logging.info("Start parsing courses\n________________________________\n")

    page_content = requests.get(BASE_URL).content
    base_soup = BeautifulSoup(page_content, "html.parser")
    courses = base_soup.select(".CourseCard_cardContainer__7_4lK")

    parsed_courses = [
        Course.get_single_course_full_details(course) for course in courses
    ]

    logging.info(
        "\n________________________________\n"
        "Parsing is finished successfully"
        "\n________________________________\n"
    )

    return parsed_courses


def write_courses_data_to_csv(
    courses: list[Course],
    output_path: str = OUTPUT_CSV_PATH,
) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(field.name for field in fields(Course))
        writer.writerows([astuple(course) for course in courses])


if __name__ == "__main__":
    courses_data = get_all_courses()
    write_courses_data_to_csv(courses_data)
