from __future__ import annotations

from dataclasses import dataclass
import re
import time
from typing import Iterable, List, Optional, Set
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


_BASE_URL = "https://mate.academy"
# Ключові слова для пошуку тривалості
_DURATION_HINTS = (
    "week",
    "weeks",
    "month",
    "months",
    "місяц",
    "місяці",
    "місяців",
    "тиж",
    "тижні",
    "тижнів",
)
_DURATION_RE = re.compile(
    r"(?i)\b(\d+(?:[.,]\d+)?)\s*("
    r"weeks?|months?|"
    r"місяц(?:і|ів)?|тиж(?:ні|нів)?"
    r")\b"
)


def _fetch_html(url: str) -> BeautifulSoup:
    """Завантажити HTML і повернути BeautifulSoup."""
    req = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; mate-scraper/1.0)"},
    )
    with urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    return BeautifulSoup(html, "html.parser")


def _select_course_cards(soup: BeautifulSoup) -> List[Tag]:
    """Підібрати можливі картки курсів різними селекторами."""
    selectors = [
        '[data-qa="course-card"]',
        '[data-test="course-card"]',
        ".course-card",
        ".CourseCard",
        'div[class*="CourseCard"]',
        'div[class*="courseCard"]',
        'article[class*="course"]',
        'a[class*="CourseCard"]',
    ]
    cards: List[Tag] = []
    seen: Set[int] = set()
    for sel in selectors:
        for el in soup.select(sel):
            if isinstance(el, Tag) and id(el) not in seen:
                seen.add(id(el))
                cards.append(el)
    if not cards:
        for section in soup.select("section"):
            if section.select_one("h2, h3") and section.select_one("p"):
                cards.append(section)
    return cards


def _text(el: Optional[Tag]) -> str:
    return el.get_text(strip=True) if isinstance(el, Tag) else ""


def _find_name(card: Tag) -> str:
    cand = (
        card.select_one('[data-qa="course-title"]')
        or card.select_one("h3")
        or card.select_one("h2")
        or card.find("header")
    )
    name = _text(cand)
    if not name:
        name = _text(card.select_one("strong")) or _text(card.select_one("a"))
    return name


def _find_description(card: Tag) -> str:
    desc = (
        card.select_one('[data-qa="course-description"]')
        or card.select_one("p")
    )
    if not desc:
        paragraphs = [p for p in card.select("p") if _text(p)]
        if paragraphs:
            desc = max(paragraphs, key=lambda p: len(_text(p)))
    text = _text(desc)
    return text[:280] if text else ""


def _find_duration(card: Tag) -> str:
    dur_el = (
        card.select_one('[data-qa="course-duration"]')
        or card.select_one('[class*="duration" i]')
        or card.select_one("time")
        or card.find(string=_DURATION_RE)
    )
    if isinstance(dur_el, Tag):
        txt = _text(dur_el)
    else:
        txt = str(dur_el) if dur_el else ""

    corpus = txt or card.get_text(" ", strip=True)
    match_obj = _DURATION_RE.search(corpus)
    if match_obj:
        num = match_obj.group(1).replace(",", ".")
        unit = match_obj.group(2).lower()
        return f"{num} {unit}"
    for hint in _DURATION_HINTS:
        if hint in corpus.lower():
            return hint
    return ""


def _extract_course(card: Tag) -> Optional[Course]:
    name = _find_name(card)
    desc = _find_description(card)
    dur = _find_duration(card)
    if not name:
        return None
    return Course(name=name, short_description=desc, duration=dur)


def _dedup_courses(courses: Iterable[Course]) -> List[Course]:
    seen: Set[str] = set()
    out: List[Course] = []
    for course_item in courses:
        key = course_item.name.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(course_item)
    return out


def get_all_courses() -> list[Course]:
    """Повертає список усіх курсів з головної mate.academy."""
    soup = _fetch_html(_BASE_URL)
    time.sleep(0.2)

    cards = _select_course_cards(soup)
    courses: List[Course] = []
    for card in cards:
        course_obj = _extract_course(card)
        if course_obj:
            courses.append(course_obj)

    return _dedup_courses(courses)
