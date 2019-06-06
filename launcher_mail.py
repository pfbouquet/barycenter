from lib.mail import MailSender
from lib.mail import send_to_group
from lib.geo_encode import address_to_geopoint

def main():

    mail_sender = MailSender('6f03cdb2c5d106f4b3407f70b27c11f7', 'e4e553e7a263b7be0ddc8292bed5fce1')

    with open('./ressources/text_mail.html') as f:
        template = f.read()

    group = \
    {
        'group_name': 'Data Scientist',
        'users': [
            {'username': 'Clement', 'email': 'clement.gain@blablacar.com'},
            {'username': 'Raph', 'email': 'raphael.berly@blablacar.com'},
            {'username': 'Clemen', 'email': 'clement.gain@hotmail.fr'}
        ]
    }

    send_to_group(mail_sender, template, group)

    print(address_to_geopoint("116 rue Salvador Allende, Nanterre"))



main()