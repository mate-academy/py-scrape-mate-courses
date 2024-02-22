from dataclasses import dataclass
from app.enums import CourseType


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
