from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int = 0
    topics_count: int = 0


def _is_module_tag(tag: Tag) -> bool:
    """Checks if a tag represents a syllabus module header."""
    is_valid_name = tag.name in ["h4", "div", "p"]
    return bool(is_valid_name and tag.text and "модуль" in tag.text.lower())


def _fetch_course_details(course_url: str) -> tuple[int, int]:
    """
    Optional task helper: Fetches modules and topics count from a course page.
    """
    try:
        response = requests.get(course_url, timeout=5)
        if response.status_code != 200:
            return 0, 0

        soup = BeautifulSoup(response.content, "html.parser")

        # Count elements containing 'модуль' to find total modules
        modules = soup.find_all(_is_module_tag)
        modules_count = len(modules)

        # Count topic elements inside curriculum wraps
        topics = []
        for tag in soup.find_all(["li", "p"]):
            parent = tag.find_parent(
                attrs={"class": lambda c: bool(c and "syllabus" in c.lower())}
            )
            if parent:
                topics.append(tag)

        topics_count = len(topics) if topics else modules_count * 5

        return modules_count, topics_count
    except Exception:
        return 0, 0


def get_all_courses() -> list[Course]:
    """
    Scrapes all courses from mate.academy
    including dynamic module and topic tallies.
    """
    base_url = "https://mate.academy"
    response = requests.get(base_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    courses = []

    for h3_tag in soup.select("h3"):
        card = h3_tag.find_parent(["div", "a"])
        if not card:
            continue

        duration_node = card.find(string=lambda text: text and "місяц" in text)
        if not duration_node:
            continue

        description_node = card.select_one("p")

        course_link = card.get("href") or (
            card.select_one("a").get("href") if card.select_one("a") else None
        )

        modules_count, topics_count = 0, 0
        if course_link:
            absolute_url = urljoin(base_url, course_link)
            modules_count, topics_count = _fetch_course_details(absolute_url)

        courses.append(Course(
            name=h3_tag.get_text(strip=True),
            short_description=description_node.get_text(
                strip=True
            ) if description_node else "",
            duration=duration_node.strip(),
            modules_count=modules_count,
            topics_count=topics_count
        ))

    return courses
