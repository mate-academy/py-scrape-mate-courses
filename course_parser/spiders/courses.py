import scrapy
import re
from course_parser.items import CourseParserItem


class CoursesSpider(scrapy.Spider):
    name = "courses"
    allowed_domains = ["mate.academy"]
    start_urls = ["https://mate.academy"]

    def parse(self, response):
        course_cards = response.css("a.ProfessionCard_cardWrapper__BCg0O")
        for card in course_cards:
            href = card.attrib.get("href")
            if not href:
                continue
            url = response.urljoin(href)
            name = (
                card.css(".ProfessionCard_title__m7uno::text")
                .get(default="N/A")
                .strip()
            )
            short_description = (
                card.css(".ProfessionCard_description__K8weo::text")
                .get(default="")
                .strip()
            )
            yield response.follow(
                url,
                self.parse_course,
                meta={"name": name, "short_description": short_description},
            )

    def parse_course(self, response):
        item = CourseParserItem()
        item["name"] = response.meta["name"]
        item["short_description"] = response.meta["short_description"]
        duration = response.css(
            "div.c-text-dark.typography_microMedium__IGlfO::text"
        ).re_first(r".*місяц.*")
        item["duration"] = duration.strip() if duration else ""
        modules = len(response.css("div.CourseModulesList_moduleListItem__b8AY9"))
        item["modules"] = modules
        topics = 0
        for p in response.css(
            "p.CourseModulesList_topicsCount__H_fv3.typography_textMain__oRJ69"
        ):
            match = re.search(r"(\d+)", p.get())
            if match:
                topics += int(match.group(1))
        item["topics"] = topics
        yield item
