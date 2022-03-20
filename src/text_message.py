import smtplib
import ssl
'''from .secrets import course_codes, Google_email, Google_password, phone_number'''

from API_calls import get_to_dos
from API_calls import clean_input
from secrets import Google_email, Google_password, phone_number, course_codes
import re



def split_messages(email_message: str) -> list:
    newline_indexes = [m.start() for m in re.finditer('\\n', email_message)]
    newline_indexes = newline_indexes[::-1]
    messages = []
    j = 0
    offset = 0

    # if index is under the 140 character limit, it contains a newline, 
    # and is above the threshold for a new message a new message will be added
    for i, _ in enumerate(email_message):
        if i % 140 + offset > 100 + offset and i in newline_indexes:
            messages.append(email_message[j:i])
            j = i
            offset += 140
    else: 
        # adds any parts of the message that the 
        messages.append(email_message[j:len(email_message)])
            
    return messages


# get to-do output from API_class module and cleans the output
to_do = get_to_dos(course_codes=course_codes)
email_message = clean_input(to_do)





if __name__ == '__main__':
    
    # set up gmail server parameters
    smtp = "smtp.gmail.com"
    port = 465


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
