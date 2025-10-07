from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int = 0

def get_all_courses() -> list[Course]:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-allow-origins=*")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(BASE_URL)
        time.sleep(3)

        wait = WebDriverWait(driver, 20)
        try:
            course_blocks = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-qa='career-path-card']"))
            )
        except TimeoutException:
            print("Courses not found on the page!")
            return []

        courses = []
        for block in course_blocks:
            try:
                name = block.find_element(By.CSS_SELECTOR, "h2[data-qa='career-path-name']").text.strip()
            except NoSuchElementException:
                name = "N/A"

            try:
                short_description = block.find_element(
                    By.CSS_SELECTOR, "p[data-qa='career-path-description']"
                ).text.strip()
            except NoSuchElementException:
                short_description = "N/A"

            try:
                duration = block.find_element(
                    By.CSS_SELECTOR, "p.CompletionProgress_progressValue__gcOy0"
                ).text.strip()
            except NoSuchElementException:
                duration = "N/A"

            try:
                modules_text = block.find_element(
                    By.CSS_SELECTOR, "div[data-qa='released-modules-count-tag'] p.Tag_text__WWT2B"
                ).text
                modules_count = int(re.search(r"\d+", modules_text).group())
            except (NoSuchElementException, AttributeError):
                modules_count = 0

            courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    duration=duration,
                    modules_count=modules_count
                )
            )

        return courses

    finally:
        driver.quit()


if __name__ == "__main__":
    all_courses = get_all_courses()
    for course in all_courses:
        print(course)
