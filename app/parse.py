from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.request import Request, urlopen


MATE_ACADEMY_URL = "https://mate.academy/"
COURSE_CARD_CLASS = "ProfessionCard_cardWrapper"
COURSE_FIELDS = {
    "ProfessionCard_title": "name",
    "ProfessionCard_description": "short_description",
    "ProfessionCard_duration": "duration",
}


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


class CoursesParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.courses: list[Course] = []
        self._course_data: dict[str, str] | None = None
        self._current_field: str | None = None

    def handle_starttag(
            self,
            tag: str,
            attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        classes = attributes.get("class", "") or ""

        if tag == "a" and COURSE_CARD_CLASS in classes:
            self._course_data = {}
            return

        if self._course_data is None:
            return

        self._current_field = next(
            (
                field
                for class_name, field in COURSE_FIELDS.items()
                if class_name in classes
            ),
            self._current_field,
        )

    def handle_data(self, data: str) -> None:
        if self._course_data is None or self._current_field is None:
            return

        value = " ".join(data.split())
        if value:
            old_value = self._course_data.get(self._current_field, "")
            self._course_data[self._current_field] = " ".join(
                part for part in (old_value, value) if part
            )

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._course_data is not None:
            required_fields = COURSE_FIELDS.values()
            if all(field in self._course_data for field in required_fields):
                self.courses.append(Course(**self._course_data))
            self._course_data = None

        if tag in {"h3", "p"}:
            self._current_field = None


def get_all_courses() -> list[Course]:
    request = Request(
        MATE_ACADEMY_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    parser = CoursesParser()

    with urlopen(request, timeout=30) as response:
        parser.feed(response.read().decode("utf-8"))

    return parser.courses
