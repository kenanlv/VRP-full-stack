from huey import MemoryHuey
from app import db
from huey import crontab
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

huey = MemoryHuey()

# @huey.periodic_task(crontab(minute='0', hour='3'))
# @huey.periodic_task(crontab(minute='*/3')) #for every three minute
@huey.periodic_task(crontab(minute='*/1'))
def every_one_minute():
    print('This task runs every six seconds')

    message = Mail(
        from_email='kelv@uw.edu',
        to_emails='conan.lee53@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        # sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)