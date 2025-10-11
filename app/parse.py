import re
import sys
import time
import random
from dataclasses import dataclass
from typing import List

import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout)
    ],
)


BASE_URL = "https://mate.academy"
COURSE_STYLE = re.compile("ProfessionCard_card")
NAME_STYLE = re.compile("ProfessionCard_title")
DURATION_STYLE = re.compile("ProfessionCard_duration")
DESCRIPTION_STYLE = re.compile("ProfessionCard_description")


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_soup(url: str) -> BeautifulSoup:
    """Fetch page content, check response, and return BeautifulSoup object."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0 Safari/537.36"
        )
    }

    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, "html.parser")

            logging.info(f"Fetched successfully: {url}")
            time.sleep(random.uniform(0.5, 1.5))  # ввічлива пауза
            return soup

        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {attempt + 1}/3 failed for {url}: {e}")
            if attempt < 2:
                time.sleep(2)
            else:
                logging.error(f"All attempts failed for {url}")
                raise


def get_field(course_soup: BeautifulSoup, style_filter: str) -> str:
    """ Get course field from BeautifulSoup object."""
    tag = course_soup.find(class_=style_filter)
    if tag is not None:
        field = tag.get_text(strip=True)
        if not field:
            logging.warning(
                f"Has not found text in tag for filter: {style_filter}"
            )
    else:
        field = ""
        logging.warning(
            f"Has not found tag in soup for filter: {style_filter}"
        )
    return field


def get_all_courses() -> List[Course]:
    courses = []
    courses_soup = get_soup(BASE_URL)
    courses_soup = courses_soup.find_all(class_=COURSE_STYLE)

    for course_soup in courses_soup:
        name = get_field(course_soup, NAME_STYLE)
        if not name:
            continue
        duration = get_field(course_soup, DURATION_STYLE)
        description = get_field(course_soup, DESCRIPTION_STYLE)

        courses.append(
            Course(
                name=name,
                short_description=(
                    description if description else "Unknown duration"
                ),
                duration=duration if duration else "Unknown duration",
            )
        )
        logging.info(f"Course {name} created successfully")
    logging.info(f"courses {courses}")
    return courses
