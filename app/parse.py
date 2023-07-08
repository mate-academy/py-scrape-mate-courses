import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    module_count: str
    topic_count: str
    duration: str


def extract_additional_info(details_url: str) -> Tuple[str, str, str]:
    details_response = requests.get(details_url)
    details_soup = BeautifulSoup(details_response.content, "html.parser")

    module_div = details_soup.find(
        "div", class_="CourseModulesHeading_modulesNumber__GNdFP"
    )
    module_count = module_div.find("p").text.split()[0] if module_div else ""

    topic_div = details_soup.find(
        "div", class_="CourseModulesHeading_topicsNumber__PXMnR"
    )
    topic_count = topic_div.find("p").text if topic_div else ""

    duration_div = details_soup.find(
        "div", class_="CourseModulesHeading_courseDuration__f_c3H"
    )
    duration = duration_div.find("p").text if duration_div else ""

    return module_count, topic_count, duration


def get_all_courses(html_content: str = None) -> List[Course]:
    base_url = "https://mate.academy"

    if html_content is None:
        response = requests.get(base_url)
        html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")
    course_elements = soup.find_all(
        "section", class_="CourseCard_cardContainer__7_4lK"
    )
    courses = []

    for course_element in course_elements:
        name_element = (
            course_element.find("span", class_="typography_landingH3__vTjok")
        ).text

        link_to_detail_info_element = course_element.select(
            "div.CourseCard_flexContainer__dJk4p > a"
        )
        link = (
            "https://mate.academy/en"
            + link_to_detail_info_element[0]["href"]
        )

        short_description_element = course_element.find(
            "p",
            class_=(
                "typography_landingMainText__Ux18x "
                "CourseCard_courseDescription__Unsqj"
            )
        )
        short_description = short_description_element.text.strip()

        if "parttime" in link:
            course_type = CourseType.PART_TIME
        else:
            course_type = CourseType.FULL_TIME

        course = Course(
            name_element, short_description, course_type,
            *extract_additional_info(link)
        )
        courses.append(course)

    return courses


def main() -> None:
    courses = get_all_courses()

    full_time_courses = [
        course for course in courses if course.course_type
        == CourseType.FULL_TIME
    ]
    part_time_courses = [
        course for course in courses if course.course_type
        == CourseType.PART_TIME
    ]

    print("Full-Time Courses:")
    for course in full_time_courses:
        print(f"Name: {course.name}")
        print(f"Description: {course.short_description}")
        print(f"Type: {course.course_type.value}")
        print(f"Module Count: {course.module_count}")
        print(f"Topic Count: {course.topic_count}")
        print(f"Duration: {course.duration}")
        print()

    print("Part-Time Courses:")
    for course in part_time_courses:
        print(f"Name: {course.name}")
        print(f"Description: {course.short_description}")
        print(f"Type: {course.course_type.value}")
        print(f"Module Count: {course.module_count}")
        print(f"Topic Count: {course.topic_count}")
        print(f"Duration: {course.duration}")
        print()


if __name__ == "__main__":
    main()
