"""
This module aims at sending mail to users.
"""

from mailjet_rest import Client
from dslib.utils.templating import render_file, render_string


class MailSender:

    def __init__(self, public_key, private_key):
        self.mailjet = Client(auth=(public_key, private_key), version='v3.1')

    def send(self, text, recipient_mail):
        """
        Send the text as an e_mail to the recipient
        :param text: text of your email
        :param recipients: list of email address of the recipients
        :return:
        """
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "smartmeetingplace@gmail.com",
                        "Name": "Smart Meeting Place"
                    },
                    "To": [
                        {
                            "Email": recipient_mail,
                            "Name": "You"
                        }
                    ],
                    "Subject": "Find out your potential meeting points!",
                    "TextPart": "Smart meeting place",
                    "HTMLPart": text
                }
            ]
        }
        result = self.mailjet.send.create(data=data)

    @staticmethod
    def generate_text(template, **params):
        """
        generate text of the email
        :param user_name: name of the user
        :param group_name: name of the group
        :param place_name: name of the place to meet
        :param place_yelp_url: url to get more details on the bar
        :param place_direction_url: link to gmaps for direction
        :return: html text to send
        """
        text = render_string(template, params)
        return text


def send_to_group(sender, template, group, place):

    group_name = group['group_name']
    user_list = group['users']
    place_name = place['name']
    place_yelp_url = place['url']
    place_direction_url = 'https: // www.google.com / maps / dir /?api = 1 & destination = {latitude}, {longitude} & travelmode = bicycling'.format(**place)

    for user in user_list:
        text = sender.generate_text(template,
                                    user_name=user['user_name'],
                                    group_name=group_name,
                                    place_name=place_name,
                                    place_yelp_url=place_yelp_url,
                                    place_direction_url=place_direction_url)
        sender.send(text, user['email'])
