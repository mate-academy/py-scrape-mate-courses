import csv
from dataclasses import astuple


def write_courses_to_csv(courses: list, csv_path: str, course_fields: list) -> None:
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(course_fields)
        writer.writerows([astuple(course) for course in courses])
