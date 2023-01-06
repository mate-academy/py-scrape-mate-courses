import sys
import time
import asyncio
import logging
from enum import Enum
from urllib.parse import urljoin
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://mate.academy"

logging.basicConfig(
    level=logging.INFO,
    format="--> %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules_number: int | None
    topics_number: int | None
    course_duration: str | None


async def get_all_courses() -> list[Course]:
    logging.info(f"Stars parsing of {BASE_URL}")
    page = httpx.get(BASE_URL).content
    logging.info(f"Get request from Mate")
    soup = BeautifulSoup(page, "html.parser")
    courses_soup = soup.select(".CourseCard_cardContainer__7_4lK")
    all_courses_info = await asyncio.gather(*[
        get_course(course_soup) for course_soup in courses_soup
    ])
    return list(all_courses_info)


async def get_course(course_soup: Tag) -> Course:
    course_info = course_soup.select_one(
        ".typography_landingH3__vTjok"
    ).text.split()
    course_url = urljoin(BASE_URL, course_soup.select_one("a")["href"])

    logging.info(f"Stars parsing details for {course_url}")
    modules_number, topics_number, course_duration = (
        await get_course_info(course_url)
    )
    logging.info(f"Get details for {course_info[1]}")

    return Course(
        name=course_info[1],
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=CourseType.PART_TIME
        if "Вечірній" in course_info
        else CourseType.FULL_TIME,
        modules_number=modules_number,
        topics_number=topics_number,
        course_duration=course_duration,
    )


async def get_course_info(course_url: str) -> tuple:
    async with httpx.AsyncClient() as client:
        response = await client.get(course_url)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")

    modules_number = int(get_course_parameter(
        soup, ".CourseModulesHeading_modulesNumber__GNdFP > p"
    ))
    topics_number = int(get_course_parameter(
        soup, ".CourseModulesHeading_topicsNumber__PXMnR > p"
    ))
    course_duration = get_course_parameter(
        soup, ".CourseModulesHeading_courseDuration__f_c3H > p"
    )

    return modules_number, topics_number, course_duration


def get_course_parameter(
        course_info_soup: BeautifulSoup,
        div_class: str
) -> str:
    course_parameter_info = course_info_soup.select_one(div_class)
    return (
        course_parameter_info.text.split()[0]
        if course_parameter_info
        else None
    )


if __name__ == "__main__":
    start = time.perf_counter()
    all_courses = asyncio.run(get_all_courses())
    for course in all_courses:
        print(course)
    end = time.perf_counter()
    print("Elapsed:", end - start)
