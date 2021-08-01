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
        'weTryContactYou': 'Wir versuchen dir innerhalb von 24 Stunden zu antworten.',
        'weReceivedAMsg': 'Wir haben eine neue Nachricht erhalten.',
        'newMsg': 'Neue Nachricht.',
        'theMsg': 'Die Nachricht',
        'from': 'Von'
    },
    'en': {
        'weReceivedYourMsg': 'We have received your message.',
        'thankYouForYourMsg': 'Thank you for your message.',
        'yourMsg': 'Your message',
        'weTryContactYou': 'We try replying within 24 hours to your message.',
        'weReceivedAMsg': 'We received a new message.',
        'newMsg': 'New message.',
        'theMsg': 'The message',
        'from': 'From'
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
                'Subject': texts['weReceivedAMsg'],
                'Variables': {
                    'title': texts['newMsg'],
                    'msgBeforeQuote': texts['theMsg'] + ':',
                    'quote': message,
                    'msgAfterQuote': texts['from'] + ' ' + sender['name'] + ', ' + sender['email']
                }
            }
        ]
    }

    client.send.create(data=data)
