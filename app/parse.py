import logging
import sys
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup as bsp4


MATE_ACADEMY_URL = "https://mate.academy"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    count_of_modules: str
    count_of_topics: str
    duration: str

    def __repr__(self):
        return f"Course: {self.name}\n" \
               f"{self.short_description}\n" \
               f"{self.type.value}\n" \
               f"{self.count_of_modules}\n" \
               f"{self.count_of_topics}\n" \
               f"{self.duration}\n" \
               f"{40 * '-'}\n"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s]: %(message)s",
    handlers=[
        logging.FileHandler("parse.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


def parse_all_pages(url) -> bsp4:
    response = requests.get(url).content
    return bsp4(response, "html.parser")


def select_from_tag(url, tag) -> str:
    info_from_tag = parse_all_pages(url).select_one(tag)
    if info_from_tag:
        return str(info_from_tag.contents[0])
    return "No time"


def get_course(course_type: CourseType):
    courses = parse_all_pages(MATE_ACADEMY_URL).select(
        f"#{course_type.value} > .cell > .CourseCard_cardContainer__7_4lK"
    )
    detail_urls = [link.select(".mb-16") for link in courses]
    all_courses = []

    for el_index in range(len(detail_urls)):

        path_to_detail = MATE_ACADEMY_URL + detail_urls[el_index][0]["href"]

        course_name = str(
            courses[el_index].select_one(
                ".typography_landingH3__vTjok"
            ).contents[0]
        )

        logging.info(f"Start parsing course: "
                     f"{' '.join(course_name.split()[1:])}")

        short_description = str(
            courses[el_index].select_one(
                ".typography_landingP1__N9PXd"
            ).contents[0]
        )

        tag_name = ".typography_landingP2__KdC5Q"

        count_of_modules = select_from_tag(
            path_to_detail,
            ".CourseModulesHeading_modulesNumber__GNdFP > "
            f"{tag_name}"
        )

        count_of_topics = select_from_tag(
            path_to_detail,
            ".CourseModulesHeading_topicsNumber__PXMnR > "
            f"{tag_name}"
        )

        duration = select_from_tag(
            path_to_detail,
            ".CourseModulesHeading_courseDuration__f_c3H > "
            f"{tag_name}"
        )

        all_courses.append(
            Course(
                name=course_name,
                short_description=short_description,
                type=course_type,
                count_of_modules=count_of_modules,
                count_of_topics=count_of_topics,
                duration=duration,
            )
        )

    return all_courses


def get_all_courses() -> list[Course]:
    return get_course(CourseType.FULL_TIME) + get_course(CourseType.PART_TIME)


if __name__ == '__main__':
    print(get_all_courses())
