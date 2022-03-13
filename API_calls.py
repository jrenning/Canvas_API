from collections import defaultdict
from secrets import API_TOKEN, course_codes

import re
import requests

# import datetime
# import pytz


def get_calender_links() -> dict:

    url = f"https://uiowa.instructure.com/api/v1/courses?access_token={API_TOKEN}"
    response = requests.get(url).json()
    links = {}

    for i, _ in enumerate(response):
        # tries to grab calender link for each class, if one does not exist skips it
        try:
            link = response[i]["calendar"]["ics"]
            course = response[i]["course_code"]
            # updates dictionary with link and course it is for
            links.update({course: link})
        except KeyError:
            pass


def get_assignments(course_codes: dict) -> dict:

    assignments = {}

    for course_name, course_code in course_codes.items():
        url = f"https://uiowa.instructure.com/api/v1/courses/{course_code}/assignments?access_token={API_TOKEN}"
        response = requests.get(url).json()
        assignment_name = []
        assignment_due_date = []

        # makes a defaultdict  with lists as inputs
        result = defaultdict(list)

        # appends due date and name to separate lists 
        for i, _ in enumerate(response):
            assignment_name.append(response[i]["name"])
            assignment_due_date.append(response[i]["due_at"])

        # pairs the assignments and the deu dates in one list
        for k, v in zip(assignment_name, assignment_due_date):
            result[k].append(v)

        assignments.update({course_name: result})

    return assignments


def get_to_dos(course_codes: dict) -> dict:

    to_do = {}

    # iterates over teh classes and course codes contained in the course list
    for course_name, course_code in course_codes.items():
        url = f"https://uiowa.instructure.com/api/v1/courses/{course_code}/todo?access_token={API_TOKEN}"
        response = requests.get(url).json()

        # makes a dictionary to store results in a list format
        result = defaultdict(list)
        assignment_name = []
        assignment_due_date = []
 
        for i, _ in enumerate(response):
            assignment_name.append(response[i]["assignment"]["name"])
            assignment_due_date.append(response[i]["assignment"]["due_at"])
         
        # appends result list with matching assignments and due dates   
        for k, v in zip(assignment_name, assignment_due_date):
            result[k].append(v)
            
        to_do.update({course_name: result})

    return to_do


def clean_input(response_dictionary: dict) -> str:

    master_assignments_dict = {}

    # groups courses with their assignments in a more parsable fromat
    for course in course_codes.keys():
        full_output = response_dictionary[course]
        values = [*full_output.values()]
        master_assignments_dict.update({course: values})

    # transform output into a string and remove unnecessary characters
    formatted_output = str(master_assignments_dict)
    patterns = ['{','}',"'"]

    for pattern in patterns:
        formatted_output = re.sub(pattern, "", formatted_output)

    formatted_output = re.sub(",", "\n", formatted_output)

    return formatted_output


if __name__ == "__main__":
    to_dos = get_to_dos(course_codes=course_codes)
    cleaned_output = clean_input(to_dos)
    print(cleaned_output)
