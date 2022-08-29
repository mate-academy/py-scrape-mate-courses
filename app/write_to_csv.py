import csv
from dataclasses import astuple

from app.parse import Course

COURSES_OUTPUT_CSV_PATH = "course.csv"
COURSES_FIELDS = [
    "name",
    "short_description",
    "type",
    "count_modules",
    "count_topics",
    "duration",
]


def write_courses_to_csv(courses: [Course]) -> None:
    with open(COURSES_OUTPUT_CSV_PATH, "w") as file:
        writer = csv.writer(file)
        writer.writerow(COURSES_FIELDS)
        writer.writerows(astuple(course) for course in courses)
