from dataclasses import dataclass
from enum import Enum


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        return cls(
            name=data["name"],
            short_description=data["short_description"],
            course_type=data["course_type"]
        )
