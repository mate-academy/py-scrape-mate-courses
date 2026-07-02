from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_soup(url: str) -> BeautifulSoup:
    text = requests.get(url).content
    return BeautifulSoup(text, "html.parser")


def get_course_links(soup: BeautifulSoup) -> list[Tag]:
    return soup.select(".TracksListV2_link__rwBFt")


def parse_course_name(link: Tag) -> str | None:
    name_tag = link.select_one(".TracksListV2_trackInfo__D0gbS")
    return name_tag.get_text(strip=True) if name_tag else None


def parse_short_description(soup: BeautifulSoup) -> str | None:
    description_tag = soup.select_one(
        ".typography_textMain__oRJ69.SalarySection_aboutProfession__C6ftM"
    )
    if not description_tag:
        return None
    return description_tag.get_text(strip=True)


def parse_duration(soup: BeautifulSoup) -> str | None:
    rows = soup.select(".TableFeedView_rowWithButtons__j6_7p")
    for row in rows:
        label = row.select_one(".typography_labelSmall__FERSi")
        value = row.select_one(".typography_microMedium__IGlfO")
        if label and value and "Тривалість" in label.get_text(strip=True):
            return value.get_text()
    return None


def parse_single_course(link: Tag) -> Course:
    detail_url = urljoin(BASE_URL, link.get("href"))
    detail_soup = get_soup(detail_url)

    return Course(
        name=parse_course_name(link),
        short_description=parse_short_description(detail_soup),
        duration=parse_duration(detail_soup),
    )


def get_all_courses() -> list[Course]:
    main_soup = get_soup(BASE_URL)
    links = get_course_links(main_soup)
    return [parse_single_course(link) for link in links]


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
