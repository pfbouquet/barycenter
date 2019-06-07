from lib.mail import MailSender
from lib.mail import send_to_group
from lib.geo_encode import address_to_geopoint
import yaml


def main():


    with open("conf/credentials.yaml", 'r') as stream:
        data_loaded_credentials = yaml.safe_load(stream)
    PUBLIC_KEY = data_loaded_credentials['mailsender']['PUBLIC_KEY']
    PRIVATE_KEY = data_loaded_credentials['mailsender']['PRIVATE_KEY']

    mail_sender = MailSender(PUBLIC_KEY, PRIVATE_KEY)

    with open('./ressources/text_mail.html') as f:
        template = f.read()

    group = \
    {
        'group_name': 'Data Scientist',
        'users': [
            {'username': 'Clement', 'email': 'clement.gain@blablacar.com'}
        ]
    }

    send_to_group(mail_sender, template, group)

    print(address_to_geopoint("116 rue Salvador Allende, Nanterre"))



main()