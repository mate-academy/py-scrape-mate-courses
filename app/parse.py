import csv
import requests
from dataclasses import dataclass, fields, astuple
from enum import Enum
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    themes: int
    duration: int


COURSE_FIELDS = [field.name for field in fields(Course)]


def get_detail_course_info(course_link: str) -> dict:
    page = requests.get(BASE_URL + course_link).content
    soup = BeautifulSoup(page, "html.parser")
    result = {
        "modules": int(soup.select_one(
            "div.CourseModulesHeading_modulesNumber__GNdFP "
            "> p.CourseModulesHeading_text__EdrEk"
        ).text.split()[0]),
        "themes": int(soup.select_one(
            "div.CourseModulesHeading_topicsNumber__PXMnR "
            "> p.CourseModulesHeading_text__EdrEk"
        ).text.split()[0]),
        "duration": int(soup.select_one(
            "div.CourseModulesHeading_courseDuration__f_c3H "
            "> p.CourseModulesHeading_text__EdrEk"
        ).text.split()[0])
    }
    return result


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    additional_info = get_detail_course_info(
        course_soup.select_one("a.CourseCard_button__HTQvE")["href"]
    )
    return Course(
        name=course_soup.select_one(
            "a > span.typography_landingH3__vTjok"
        ).text,
        short_description=course_soup.select_one(
            ".typography_landingMainText__Ux18x"
        ).text,
        course_type=(
            CourseType.PART_TIME
            if course_soup.select(".Button_black__kAQvx")
            else CourseType.FULL_TIME),
        modules=additional_info["modules"],
        themes=additional_info["themes"],
        duration=additional_info["duration"]
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses_soup = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course_soup) for course_soup in courses_soup]


def write_courses_to_csv(courses: list[Course], path: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def remove_empty_rows(filename: str) -> None:
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    non_empty_lines = [line.strip() for line in lines if line.strip()]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(non_empty_lines))


def main(output_csv_path: str) -> None:
    write_courses_to_csv(get_all_courses(), output_csv_path)
    remove_empty_rows(output_csv_path)


if __name__ == "__main__":
    main("courses.csv")
