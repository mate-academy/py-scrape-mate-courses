from bs4 import BeautifulSoup
import requests

root = "https://mate.academy/"
website = f'{root}/courses'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, "html.parser")

box = soup.find(class_='cell large-6 large-offset-1 mb-32')

links = [link['href'] for link in box.find_all('a', class_='mb-16', href=True)]

for link in links:
    result = requests.get(f'{root}/{link}')
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
