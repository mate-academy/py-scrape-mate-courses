import csv

FOR_SURE_THIS_COURSES = [
    "QA",
    "Java",
    "Python",
    "Recruiter",
    "DevOps",
    "Digital",
    "Data"
]

def test_get_all_courses():
    with open("../courses.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        course_names = [row["name"] for row in reader]
    for course in FOR_SURE_THIS_COURSES:
        assert any(
            course.lower() in course_name.lower() for course_name in course_names
        ), f"Course '{course}' have not been parsed"
