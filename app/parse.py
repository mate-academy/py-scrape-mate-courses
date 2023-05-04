# import requests
# from bs4 import BeautifulSoup
# from dataclasses import dataclass
# from enum import Enum
#
#
# class CourseType(Enum):
#     FULL_TIME = "full-time"
#     PART_TIME = "part-time"
#
#
# @dataclass
# class Course:
#     name: str
#     short_description: str
#     course_type: CourseType
#
#
# url = "https://mate.academy"
# r = requests.get(url)
# soup = BeautifulSoup(r.content, "html.parser")
#
# def get_full_time():
#     full_time_courses = soup.find("div", {"id": "full-time"})
#     courses = full_time_courses.find_all("section", {"class": "CourseCard_cardContainer__7_4lK"})
#     for course in courses:
#         title = course.find("span", {"class": "typography_landingH3__vTjok"}).text
#         description = course.find("p", {
#             "class": "typography_landingMainText__Ux18x CourseCard_courseDescription__Unsqj"}).text
#         result = Course(
#             name=title,
#             short_description=description,
#             course_type=CourseType.FULL_TIME
#         )
#         # print(f"Title: {title}\nDescription: {description}\n")
#         return result
#
# def get_part_time():
#     full_time_courses = soup.find("div", {"id": "full-time"})
#     courses = full_time_courses.find_all("section", {"class": "CourseCard_cardContainer__7_4lK"})
#     for course in courses:
#         title = course.find("span", {"class": "typography_landingH3__vTjok"}).text
#         description = course.find("p", {
#             "class": "typography_landingMainText__Ux18x CourseCard_courseDescription__Unsqj"}).text
#         result = Course(
#             name=title,
#             short_description=description,
#             course_type=CourseType.PART_TIME
#         )
#         # print(f"Title: {title}\nDescription: {description}\n")
#         return result
#
# def get_all_courses():
#     result = []
#     result.append(get_full_time(),)
#     result.append(get_part_time())
#     return result
#
# print(get_all_courses())
#
# part_time_courses = soup.find("div", {"id": "part-time"})
# course_sections = part_time_courses.find_all('section', class_='CourseCard_cardContainer__7_4lK')
#
#
# for course in course_sections:
#     title = course.find("span", {"class": "typography_landingH3__vTjok"}).text
#     description = course.find("p", {"class": "typography_landingMainText__Ux18x CourseCard_courseDescription__Unsqj"}).text
#     print(f"Title: {title}\nDescription: {description}\n")

import time
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from dataclasses import dataclass
# from enum import Enum
#
#
# class CourseType(Enum):
#     FULL_TIME = "full-time"
#     PART_TIME = "part-time"
#
#
# @dataclass
# class Course:
#     name: str
#     short_description: str
#     course_type: CourseType
#
#
# url = "https://mate.academy"
# driver = webdriver.Chrome()
# driver.get(url)
# soup = BeautifulSoup(driver.page_source, "html.parser")
#
#
# def get_full_time():
#     full_time_courses = soup.find("div", {"id": "full-time"})
#     courses = full_time_courses.find_all("section", {"class": "CourseCard_cardContainer__7_4lK"})
#     for course in courses:
#         title = course.find("span", {"class": "typography_landingH3__vTjok"}).text
#         description = course.find("p", {
#             "class": "typography_landingMainText__Ux18x CourseCard_courseDescription__Unsqj"}).text
#         result = Course(
#             name=title,
#             short_description=description,
#             course_type=CourseType.FULL_TIME
#         )
#         print(f"Title: {title}\nDescription: {description}\n")
#
#
# def get_part_time():
#     part_time_courses = soup.find("div", {"id": "part-time"})
#     courses = part_time_courses.find_all("section", {"class": "CourseCard_cardContainer__7_4lK"})
#     for course in courses:
#         title = course.find("span", {"class": "typography_landingH3__vTjok"}).text
#         description = course.find("p", {
#             "class": "typography_landingMainText__Ux18x CourseCard_courseDescription__Unsqj"}).text
#         result = Course(
#             name=title,
#             short_description=description,
#             course_type=CourseType.PART_TIME
#         )
#         print(f"Title: {title}\nDescription: {description}\n")
#         # return result
#
#
# def get_all_courses():
#     get_full_time()
#     get_part_time()
#
#
# # def get_all_courses():
# #     result = []
# #     result.append(get_full_time(),)
# #     result.append(get_part_time())
# #     return result
#
# print(get_all_courses())
#
# # Close the browser
# driver.quit()
from selenium import webdriver
from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


url = "https://mate.academy"
driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")


def get_courses(course_type):
    courses_list = []
    courses = soup.find("div", {"id": course_type.value})
    courses = courses.find_all("section", {"class": "CourseCard_cardContainer__7_4lK"})
    for course in courses:
        title = course.find("span", {"class": "typography_landingH3__vTjok"}).text
        description = course.find("p", {"class": "typography_landingMainText__Ux18x CourseCard_courseDescription__Unsqj"}).text
        course = Course(name=title, short_description=description, course_type=course_type)
        courses_list.append(course)
    return courses_list


def get_all_courses():
    all_courses = []
    all_courses.extend(get_courses(CourseType.FULL_TIME))
    all_courses.extend(get_courses(CourseType.PART_TIME))
    return all_courses


courses = get_all_courses()
for course in courses:
    print(f"Title: {course.name}\nDescription: {course.short_description}\n")

driver.quit()
