import requests
from bs4 import BeautifulSoup, Tag

from app.config import BASE_URL
from app.enums import CourseType
from app.models import Course


class MateScrapper:

    @staticmethod
    def check_course_type(course_soup: Tag) -> list[CourseType]:
        full_time_path = course_soup.select(".ButtonBody_buttonText__FMZEg")

        if len(full_time_path) == 2:
            return [CourseType.FULL_TIME, CourseType.PART_TIME]

        if full_time_path[0].text == "Власний темп":
            return [CourseType.PART_TIME]

        return [CourseType.FULL_TIME]

    def parse_course(self, course_soup: Tag) -> list[Course]:
        name = course_soup.select_one("h3").text,
        name = name[0]
        short_description = course_soup.select_one(".mb-32").text,
        short_description = short_description[0]
        course_types = self.check_course_type(course_soup)

        courses = []

        for course_type in course_types:
            courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=course_type,
                )
            )

        return courses

    def get_all_courses(self) -> list[Course]:
        page = requests.get(BASE_URL).content
        soup = BeautifulSoup(page, "html.parser")

        courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

        all_courses = []

        for course in courses_soup:
            all_courses.extend(self.parse_course(course))

        return all_courses
