from app.scrapper import MateScrapper
from app.models import Course


def parse() -> list[Course]:
    scrapper = MateScrapper()
    all_courses = scrapper.get_all_courses()

    return all_courses


if __name__ == "__main__":
    print(parse())
