from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Substitution
from python_http_client import exceptions
import os
import json
import math


def send_email(identifier, email, phone=None, time=None, sub_user=None):
    # template_list_id = [0,1,2]
    template_list_id = ['d-c37816845b1447c892c7db79f393dc54', 'd-13dc2f2deda6425481cd74f18c61cc33',
                        'd-6cd5efc8410d469795cd6b6709dbc2ff']
    message = Mail(
        from_email='vrp.support@wow.com',
        to_emails=email)
    subject = 'Event Pick Up Info'
    # for user
    if identifier == 'User':
        template_data = {'phone': phone, 'time': '10:' + str(math.ceil(time))}
        id_idx = 0
    else:
        template_data = {}
        for i in range(len(sub_user['name'])):
            template_data['name' + str(i)] = sub_user['name'][i]
            template_data['phone' + str(i)] = sub_user['phone'][i]
            template_data['address' + str(i)] = sub_user['address'][i]
        id_idx = 1 if len(template_data) == 0 else 2
    message.dynamic_template_data = template_data

    template_id = template_list_id[id_idx]
    message.template_id = template_id
    print('temp_data')
    print(template_data)
    print('temp_idx', id_idx)
    # message.dynamic_template_data = {
    #     'subject': 'Testing Templates',
    #     'name': 'BaBaYeGa',
    #     'name1': 'Costume Name',
    #     'name2': 'Josh Wick'
    # }
    # data={"name", "address", "phone", "time"}

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        print('sending email to ' + identifier)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except exceptions.BadRequestsError as e:
        print(e.body)
