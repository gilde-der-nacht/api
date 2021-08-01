#!/usr/bin/env python3

# import the mailjet wrapper
from mailjet_rest import Client

mail_template = {
    'gilde': 2939493,
    'spieltage': 2939553,
    'rollenspieltage': 2939557
}


i18n = {
    'de': {
        'weReceivedYourMsg': 'Wir haben deine Nachricht erhalten.',
        'thankYouForYourMsg': 'Vielen Dank für deine Nachricht.',
        'yourMsg': 'Deine Nachricht',
        'weTryContactYou': 'Wir versuchen dir innerhalb von 24 Stunden zu antworten.'
    },
    'en': {
        'weReceivedYourMsg': 'We have received your message.',
        'thankYouForYourMsg': 'Thank you for your message.',
        'yourMsg': 'Your message',
        'weTryContactYou': 'We try replying within 24 hours to your message.'
    }
}


def config(public_key, private_key, version):
    return Client(auth=(public_key, private_key), version=version)


def mail_send(client, message, sender, recipient, template, language='de'):
    texts = i18n[language]

    data = {
        'Messages': [
            {
                'To': [
                    {
                    'Email': sender['email'],
                    'Name': sender['name']
                    }
                ],
                'TemplateID': mail_template.get(template),
                'TemplateLanguage': True,
                'Subject': texts['weReceivedYourMsg'],
                'Variables': {
                    'title': texts['thankYouForYourMsg'],
                    'msgBeforeQuote': texts['yourMsg'] + ':',
                    'quote': message,
                    'msgAfterQuote': texts['weTryContactYou']
                }
            },
            {
                'To': [
                    {
                    'Email': recipient['email'],
                    'Name': recipient['name']
                    }
                ],
                'ReplyTo': {
                    'Email': sender['email'],
                    'Name': sender['name']
                },
                'TemplateID': mail_template.get(template),
                'TemplateLanguage': True,
                'Subject': 'Wir haben eine neue Nachricht erhalten.',
                'Variables': {
                    'title': 'Neue Nachricht.',
                    'msgBeforeQuote': 'Die Nachricht:',
                    'quote': message,
                    'msgAfterQuote': 'Von ' + sender['name'] + ', ' + sender['email']
                }
            }
        ]
    }

    client.send.create(data=data)
