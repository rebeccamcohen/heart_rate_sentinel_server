import sendgrid
import os
from sendgrid.helpers.mail import *


def send_email(patient_id, time_stamp):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("rmcohen100@gmail.com")
    to_email = Email("rmc50@duke.edu")
    subject = "patient {} is tachycardic".format(patient_id)
    content = Content("text/plain", "patient {} measured a tachycardic heart rate ({})".format(patient_id, time_stamp))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
