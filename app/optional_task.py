from bs4 import BeautifulSoup
import requests

ROOT = "https://mate.academy/"
WEBSITE = f'{ROOT}/courses'

result = requests.get(WEBSITE)
content = result.text
soup = BeautifulSoup(content, "html.parser")
box = soup.find(class_='cell large-6 large-offset-1 mb-32')
links = [link['href'] for link in box.find_all('a', class_='mb-16', href=True)]


def course_detailed_info():
    for link in links:
        result = requests.get(f'{ROOT}/{link}')
        content = result.text
        soup = BeautifulSoup(content, "html.parser")

        name = str(link).split("/")[-1]

        num_modules = soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP > p"
        ).text

        num_topics = soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR > p"
        ).text

        duration = soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H > p"
        ).text

        print(f"{name}: {num_modules}, {num_topics}, {duration}")


course_detailed_info()
