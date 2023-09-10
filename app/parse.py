import requests
from bs4 import BeautifulSoup

from course import Course, CourseType


URL = "https://mate.academy/"


def parse() -> list[dict]:
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
    data_list = parse()

    return [
        Course.from_dict(data) for data in data_list
    ]


if __name__ == "__main__":
    print(get_all_courses())
