from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"

CSS_SELECTORS = {
    "course_card": ".ProfessionCard_cardWrapper__BCg0O"
                   ".ProfessionsListSectionTemplate_card__ZNsgf",
    "name": ".ProfessionCard_title__m7uno"
            ".typography_headingLarge__6__NS"
            ".typography_medium_headingMedium__i8C3Z",
    "description": ".typography_paragraphMedium__FWO7K"
                   ".ProfessionCard_text___l0Du"
                   ".ProfessionCard_description__K8weo",
    "duration": ".typography_paragraphMedium__FWO7K"
                ".ProfessionCard_text___l0Du"
                ".ProfessionCard_duration__13PwX"
}


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    pass
