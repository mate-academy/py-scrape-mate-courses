import asyncio
import time

from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from httpx import AsyncClient


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    count_modules: int
    count_topics: int
    count_duration: str


async def parse_single_course(
        course_soup: BeautifulSoup,
        course_detail_soup: BeautifulSoup
) -> Course:
    return Course(
        name=course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text.split()[1],
        short_description=course_soup.select_one(
            ".typography_landingP1__N9PXd"
        ).text,
        course_type=CourseType.PART_TIME if course_soup.select_one(
            ".typography_landingH3__vTjok"
        ).text.split()[-1] == "Вечірній" else CourseType.FULL_TIME,
        count_modules=int(course_detail_soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP > "
            ".typography_landingP2__KdC5Q"
        ).text.split()[0]),
        count_topics=int(course_detail_soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR > "
            ".typography_landingP2__KdC5Q"
        ).text.split()[0]),
        count_duration="Not indicated" if len(course_detail_soup) == 2 else
        course_detail_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H > "
            ".typography_landingP2__KdC5Q"
        ).text.split()[0],
    )


async def get_courses_detail(
        course_soup: BeautifulSoup,
        client: AsyncClient
) -> list[BeautifulSoup]:
    link_course = urljoin(BASE_URL, course_soup.select_one("a")["href"])
    page = await client.get(link_course)
    page_soup = BeautifulSoup(page.content, "html.parser")
    return page_soup.select(".CourseModulesHeading_headingGrid__50qAP")


async def get_courses(client: AsyncClient) -> list[BeautifulSoup]:
    page = await client.get(BASE_URL)
    page_soup = BeautifulSoup(page.content, "html.parser")
    return page_soup.select(".CourseCard_cardContainer__7_4lK")


async def get_all_courses() -> list[Course]:
    async with AsyncClient() as client:
        courses = await get_courses(client)

        list_courses = []

        for course_soup in courses:
            courses_detail_soup = await get_courses_detail(course_soup, client)
            for course_detail in courses_detail_soup:
                result = await asyncio.gather(
                    parse_single_course(course_soup, course_detail)
                )
                list_courses.extend(result)
        return list_courses


if __name__ == "__main__":
    start = time.perf_counter()

    courses = asyncio.run(get_all_courses())
    for course in courses:
        print(course)

    print(f"Elapsed: {time.perf_counter() - start}")
