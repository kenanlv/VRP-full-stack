from huey import MemoryHuey
from app import db
from huey import crontab
import os
from test import solving_for_route
from email_sender_helper import send_email
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Substitution
from python_http_client import exceptions
import json

huey = MemoryHuey()


# @huey.periodic_task(crontab(minute='0', hour='3'))
# @huey.periodic_task(crontab(minute='*/3')) #for every three minute
@huey.periodic_task(crontab(minute='*/1'))
def every_one_minute():
    print('This task runs every six seconds')
    # html_message = open('driver_email.html').read()
    candi_info = solving_for_route()
    email = candi_info['user_info']['email_list']
    user_address = candi_info['user_info']['locations_txt']
    user_name = candi_info['user_info']['name']
    phone = candi_info['user_info']['phone_num']
    time_cost = candi_info['user_info']['time_cost']
    for path in candi_info['path']:
        sub_user = {'name': [], 'phone': [], 'address': []}
        time = 0
        for i in range(1, len(path) - 1):
            time += time_cost[path[i - 1]][path[i]]
            send_email(identifier='User', email=email[path[i]], phone=phone[path[0]], time=time)
            sub_user['name'].append(user_name[path[i]])
            sub_user['phone'].append(phone[path[i]])
            sub_user['address'].append(user_address[path[i]])
        send_email(identifier='Driver', email=email[path[0]], sub_user=sub_user)

    data = {
        "from": {
            "email": "conan.lee53@gmail.com",
            "name": "Sam Smith"
        },
        "personalizations": [
            {
                "to": [
                    {
                        "email": "kelv@uw.edu",
                        "name": "John Doe"
                    }
                ]
            }
        ],
        "template_id": "d-6cd5efc8410d469795cd6b6709dbc2ff",
        "name": "bababyefu",
        "city": "Russia",
        "subject": "Hello, World!"
    }
