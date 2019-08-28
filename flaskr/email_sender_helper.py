from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Substitution
from python_http_client import exceptions
import json


def send_email(identifier, email, phone=None, time=None, sub_user=None):
    template_list_id = [0,1,2,3,4,5,6]
    message = Mail(
        from_email='vrp.support@wow.com',
        to_emails=email)
    subject = 'Event Pick Up Info'
    # for user
    if identifier == 'User':
        template_data = {'phone': phone, 'time': time}
        id_idx = 5
    else:
        template_data = {}
        if sub_user:
            id_idx = len(sub_user['name'])
            for i in range(len(sub_user['name'])):
                template_data['name' + str(i)] = sub_user['name'][i]
                template_data['phone' + str(i)] = sub_user['phone'][i]
                template_data['address' + str(i)] = sub_user['address'][i]
        else:
            id_idx = 0
    message.dynamic_template_data = template_data

    template_id = template_list_id[id_idx]
    message.template_id = template_id
    print(template_data)
    # message.dynamic_template_data = {
    #     'subject': 'Testing Templates',
    #     'name': 'BaBaYeGa',
    #     'name1': 'Costume Name',
    #     'name2': 'Josh Wick'
    # }
    # data={"name", "address", "phone", "time"}

    # try:
    #     sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    #     print('sending email to '+ identifier)
    #     response = sg.send(message)
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)
    # except exceptions.BadRequestsError as e:
    #     print(e.body)
