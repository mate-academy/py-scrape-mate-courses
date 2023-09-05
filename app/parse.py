from dataclasses import fields

from app.courses import get_all_courses, Course
from app.utils import write_courses_to_csv


COURSE_FIELDS = [course_field.name for course_field in fields(Course)]


def main(courses_csv_path: str):
    courses = get_all_courses()
    write_courses_to_csv(courses, courses_csv_path, COURSE_FIELDS)


if __name__ == "__main__":
    main("courses.csv")
