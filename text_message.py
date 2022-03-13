import smtplib
import ssl
from secrets import Google_email, Google_password, phone_number, course_codes
from API_calls import get_to_dos
from API_calls import clean_input

# set up gmail server parameters
smtp = "smtp.gmail.com"
port = 465

# get to-do output from API_class module and cleans the output
to_do = get_to_dos(course_codes=course_codes)
email_message = clean_input(to_do)

# using ssl login to the gmail server and send a message 
with smtplib.SMTP_SSL(smtp, port, context=ssl.create_default_context()) as email:
    email.login(Google_email, Google_password)
    # sender, receiver, message
    email.sendmail(Google_email, phone_number, email_message)
