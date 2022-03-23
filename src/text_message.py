import smtplib
import ssl

from API_calls import get_to_dos
from API_calls import clean_input
from secrets import Google_email, Google_password, phone_number, course_codes
import re





def split_messages(email_message: str) -> list:
    
    # find all newlines to find points at which to break up the message
    newline_indices = [m.start() for m in re.finditer('\\n', email_message)]

    chosen_newline_indices = []
    messages = []


    # starting count at limit of message length
    count = 140

    # loops through the message and starts looking for the most optimal newlines to cut at (ie closest to the 140 limit)
    # counts down from the limit until an index is found, 
    # adds the index to a list of chosen indexes then adds the indexes value to the limit and counts down again
    for counter, _ in enumerate(email_message):
        for index in newline_indices:
            if index == count:
                chosen_newline_indices.append(index)
                count = 140 + index
        count -= 1

    # starting index value
    i = 0

    # makes messages from chosen newline indices
    for index in chosen_newline_indices:
        messages.append(email_message[i: index])
        i = index

            
    return messages



if __name__ == '__main__':
    
    # set up gmail server parameters
    smtp = "smtp.gmail.com"
    port = 465

    to_do = get_to_dos(course_codes)
    email_message = clean_input(to_do)

    messages = split_messages(email_message=email_message)

    # add newlines to the start of each message to avoid the addition of 
    # X-CMAE envelope to the text messages
    for i, message in enumerate(messages):
        messages[i] = '\n\n\n' + message
            

    # using ssl login to the gmail server and send a message 
    with smtplib.SMTP_SSL(smtp, port, context=ssl.create_default_context()) as email:
        email.login(Google_email, Google_password)
        # sender, receiver, message
        for message in messages:
            if len(message) > 1:
                email.sendmail(Google_email, phone_number, message)
