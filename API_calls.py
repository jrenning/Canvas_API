
from doctest import master
import pprint
from collections import defaultdict
from datetime import datetime
from secrets import API_TOKEN, course_codes

import pytz
import re
import requests

url = f"https://uiowa.instructure.com/api/v1/courses/181937/assignments?access_token={API_TOKEN}"

response = requests.get(url).json()


def get_calender_links(url):
    response = requests.get(url).json()
    links = {}
    for i, _ in enumerate(response):
        # tries to grab calender link for each class, if one does not exist skips it
        try:
            link = response[i]["calendar"]["ics"]
            course = response[i]["course_code"]
            links.update({course: link})
        except KeyError:
            pass


def get_assignments(course_codes):
    assignments = {}
    for course_name, course_code in course_codes.items():
        url = f"https://uiowa.instructure.com/api/v1/courses/{course_code}/assignments?access_token={API_TOKEN}"
        response = requests.get(url).json()
        name = course_name
        assignment_name = []
        assignment_due_date = []
        result = defaultdict(list)
        for i, _ in enumerate(response):
            assignment_name.append(response[i]["name"])
            assignment_due_date.append(response[i]["due_at"])
        for k, v in zip(assignment_name, assignment_due_date):
            result[k].append(v)
        assignments.update({name: result})

    return assignments


def get_to_dos(course_codes):
    to_do = {}
    for course_name, course_code in course_codes.items():
        url = f"https://uiowa.instructure.com/api/v1/courses/{course_code}/todo?access_token={API_TOKEN}"
        response = requests.get(url).json()
        name = course_name
        result = defaultdict(list)
        assignment_name = []
        assignment_due_date = []
        for i, _ in enumerate(response):
            assignment_name.append(response[i]["assignment"]["name"])
            assignment_due_date.append(response[i]["assignment"]["due_at"])
        for k, v in zip(assignment_name, assignment_due_date):
            result[k].append(v)
        to_do.update({name: result})

    return to_do

def clean_input(response_dictionary: dict):
    master_assignments = {}

    for course in course_codes.keys():
        full_output = response_dictionary[course]
        master_assignments.update({course: (full_output.keys(), full_output.values())})
    for key, value in master_assignments.items():
        pass
    
    return str(master_assignments)
    


if __name__ == "__main__":
    to_dos = get_to_dos(course_codes=course_codes)
    
            
