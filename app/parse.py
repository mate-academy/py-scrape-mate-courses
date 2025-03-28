from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"

CSS_SELECTORS = {
    "course_card": ".ProfessionCard_cardWrapper__BCg0O"
                   ".ProfessionsListSectionTemplate_card__ZNsgf",
    "name": ".ProfessionCard_title__m7uno"
            ".typography_headingLarge__6__NS"
            ".typography_medium_headingMedium__i8C3Z",
    "description": ".typography_paragraphMedium__FWO7K"
                   ".ProfessionCard_text___l0Du"
                   ".ProfessionCard_description__K8weo",
    "duration": ".typography_paragraphMedium__FWO7K"
                ".ProfessionCard_text___l0Du"
                ".ProfessionCard_duration__13PwX"
}


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(CSS_SELECTORS["name"]).text,
        short_description=course.select_one(CSS_SELECTORS["description"]).text,
        duration=course.select_one(CSS_SELECTORS["duration"]).text
    )


def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def get_all_courses() -> list[Course]:
    soup = fetch_page(BASE_URL)
    courses = soup.select(CSS_SELECTORS["course_card"])

    return [parse_single_course(course) for course in courses]


def main() -> None:
    courses = get_all_courses()
    print(courses)


if __name__ == "__main__":
    main()
