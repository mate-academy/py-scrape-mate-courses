import sys
import time
import random
from dataclasses import dataclass
import requests
import logging
from urllib.parse import urljoin
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


def get_all_courses() -> list[Course]:
    courses = []
    courses_soup = get_soup(BASE_URL)
    raw_courses = courses_soup.select(".ProfessionCard_cardWrapper__BCg0O")

    for raw_course in raw_courses:
        raw_name = raw_course.select_one(
            ".ProfessionCard_title__m7uno"
            ".typography_captionLarge__fZ9ls"
            ".typography_medium_captionMedium__MVxkq"
        )
        if raw_name is not None:
            name = raw_name.text if raw_name.text is not None else None
        else:
            logging.warning("Couldn't find text name, skipping")
            continue

        raw_duration = raw_course.select_one(
            ".typography_paragraphMedium__FWO7K."
            "ProfessionCard_text___l0Du.ProfessionCard_duration__13PwX"
        )
        if raw_duration is not None:
            duration = (
                raw_duration.text
                if raw_duration.text is not None
                else "unknown"
            )
        else:
            duration = "unknown"
            logging.warning(
                f"Has not found duration for course {name}, "
                f"input 'unknown"
            )

        href = raw_course.get("href")
        if href is None:
            description = "no description"
            logging.warning(f"Link not found for {name}")

        else:
            course_url = urljoin(BASE_URL, href)
            course_soup = get_soup(course_url)

            raw_description = course_soup.select_one(
                "p.typography_textMain__oRJ69"
                ".SalarySection_aboutProfession__C6ftM"
            )

            if raw_description is not None:
                description = (
                    raw_description.text
                    if raw_description.text
                    else "No description"
                )
        if description == "No description":
            logging.warning(
                f"Couldn't find description for course {name}, "
                f"input 'No description')"
            )
        courses.append(
            Course(
                name=name,
                short_description=description,
                duration=duration
            )
        )
        logging.info(f"Course {name} created successfully")
    logging.info(f"courses {courses}")
    return courses
