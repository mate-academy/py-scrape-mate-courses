from dataclasses import dataclass

import requests
from parsel import Selector


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


class CoursesSpider:
    URL = "https://mate.academy/"

    @staticmethod
    def get_html() -> str:
        return requests.get(CoursesSpider.URL).text

    @staticmethod
    def extract_text(course, selector: str) -> str:
        return course.css(selector).get()

    @staticmethod
    def parse_course(course) -> Course:
        return Course(
            name=CoursesSpider.extract_text(
                course,
                ".ProfessionCard_title__m7uno span::text"
            ),
            short_description=CoursesSpider.extract_text(
                course,
                ".ProfessionCard_description__K8weo::text"
            ),
            duration=CoursesSpider.extract_text(
                course,
                ".ProfessionCard_duration__13PwX::text"
            ),
        )

    @staticmethod
    def parse():
        html = CoursesSpider.get_html()
        selector = Selector(html)

        courses = selector.css(".ProfessionCard_cardWrapper__BCg0O")

        return [CoursesSpider.parse_course(course) for course in courses]