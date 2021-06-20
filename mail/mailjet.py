#!/usr/bin/env python3

# import the mailjet wrapper
from mailjet_rest import Client
import os

mail_template = {
    'gilde': 2939493,
    'spieltage': 2939553,
    'rollenspieltage': 2939557
}


def config(public_key, private_key, version):
    return Client(auth=(public_key, private_key), version=version)


def mail_send(client, message, sender, recipient, template):
    data = {
        'Messages': [
            {
                'To': [
                    {
                    'Email': sender['mail'],
                    'Name': sender['name']
                    }
                ],
                'TemplateID': mail_template.get(template),
                'TemplateLanguage': true,
                'Subject': 'Wir haben deine Nachricht erhalten.',
                'Variables': {
                    'title': 'Vielen Dank für deine Nachricht.',
                    'msgBeforeQuote': 'Deine Nachricht:',
                    'quote': message,
                    'msgAfterQuote': 'Wir versuchen dir innerhalb von 24 Stunden zu antworten.'
                }
            },
            {
                'To': [
                    {
                    'Email': recipient['mail'],
                    'Name': recipient['name']
                    }
                ],
                'ReplyTo': {
                    'Email': sender['mail'],
                    'Name': sender['name']
                },
                'TemplateID': mail_template.get(template),
                'TemplateLanguage': true,
                'Subject': 'Wir haben eine neue Nachricht erhalten.',
                'Variables': {
                    'title': 'Neue Nachricht.',
                    'msgBeforeQuote': 'Die Nachricht:',
                    'quote': message,
                    'msgAfterQuote': 'Von ' + sender['name'] + ', ' + sender['mail']
                }
            }
        ]
    }

    client.send.create(data=data)
