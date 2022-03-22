from collections import defaultdict
'''from .secrets import API_TOKEN, course_codes'''
from secrets import API_TOKEN, course_codes

import re
import requests
import datetime



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

    master_assignments_list = []
    
    # append each course along with the assignments and due dates to a list in order 
    for course_name in course_codes.keys():
        master_assignments_list.append( course_name + ':')
        for k, v in response_dictionary[course_name].items():
            master_assignments_list.append(str(k))
            master_assignments_list.append(str(v))

    # take out brackets and apostrophes from date format to allow for parsing into readable format
    patterns = ["'","\[","\]"]
    for i, _ in enumerate(master_assignments_list):
        for pattern in patterns:
            master_assignments_list[i] = re.sub(pattern, "", master_assignments_list[i])


    for i, input in enumerate(master_assignments_list):
        # matches on ISO-8 time formats 
        if re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?', input):
            initial_time = datetime.datetime.strptime(input, "%Y-%m-%dT%H:%M:%S%z")
            
            # APi adds 5 hours to actual due date time for some reason, so this adds them back
            initial_time = initial_time - datetime.timedelta(hours=5)

            # changes to 12 hour time system
            if initial_time.hour > 12:
                final_time = initial_time - datetime.timedelta(hours=12)
                new_output = final_time.strftime(' %a %b %d %H:%Mpm')
            else:
                new_output = initial_time.strftime(' %a %b %d %H:%Mam')

            master_assignments_list[i] = new_output


    final_string = ''

    # concatonate the assignments into one string
    for record in master_assignments_list:
        final_string += record

    # split up lines after courses, then after assignments
    final_string = re.sub('(\D:)','\\1\n',final_string)
    final_string = re.sub('([0-9]{2}pm|[0-9]{2}am)', '\\1\n', final_string)
    
    return final_string


if __name__ == "__main__":
    to_dos = get_to_dos(course_codes=course_codes)
    cleaned_output = clean_input(to_dos)
    print(cleaned_output)
