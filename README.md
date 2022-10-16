# Scrape mate courses

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start

## Task

Get list of all full-time & part-time courses on the landing page of [mate.academy](https://mate.academy
) website. Each course should have `name`, `short_description` and `course_type`(full-time or part-time). 
The structure of classes is already implemented in `app/parse.py`. 
So your task is to implement `get_all_courses` function to parse all these courses.

Hints:
- Make your code `DRY`, `KISS` and follow `SRP` principle (single-responsibility).
- Implement the simplest solution you could find.


### Optional task:

Also get info about count of `modules`, count of `topics` and `duration` for each course.

