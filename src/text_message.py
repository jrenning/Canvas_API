import smtplib
import ssl
from secrets import Google_email, Google_password, phone_number, course_codes
from src.API_calls import get_to_dos
from src.API_calls import clean_input

# set up gmail server parameters
smtp = "smtp.gmail.com"
port = 465

# get to-do output from API_class module and cleans the output
to_do = get_to_dos(course_codes=course_codes)
email_message = clean_input(to_do)

messages = []
count = 0

def split_messages(email_message):
    # splits the messages into multiple oens to stay below the character limit on text messages 
    for i,character in enumerate(email_message):
        if i % 100 > 80 and character == '\n' and count == 0:
            messages.append(email_message[0:i])
            j = i
            count += 1
        if i % 100 > 80 and character == '\n' and count == 1:
            messages.append(email_message[j:i])
    return messages

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
