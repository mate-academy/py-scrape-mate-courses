from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_page() -> list[dict]:
    page_content = requests.get(URL).content
    page_soup = BeautifulSoup(page_content, "html.parser")

    containers = page_soup.find_all(
        class_="CourseCard_cardContainer__7_4lK"
    )

    data = []
    for container in containers:
        course_name = container.select(".typography_landingH3__vTjok")[0].text
        course_description = container.select(
            ".CourseCard_courseDescription__Unsqj"
        )[0].text

        if container.find_parent(id="full-time"):
            course_type = CourseType("full-time")
        else:
            course_type = CourseType("part-time")

        data.append(
            {
                "name": course_name,
                "short_description": course_description,
                "course_type": course_type
            }
        )
    return data


def get_all_courses() -> list[Course]:
    data_list = parse_page()

    return [
        Course(
            name=data["name"],
            short_description=data["short_description"],
            course_type=data["course_type"]
        ) for data in data_list
    ]


if __name__ == "__main__":
    print(get_all_courses())
