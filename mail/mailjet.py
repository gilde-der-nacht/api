#!/usr/bin/env python3

# import the mailjet wrapper
from mailjet_rest import Client

mail_template = {
    'gilde': 2939493,
    'spieltage': 2939553,
    'rollenspieltage': 2939557,
    'tabletoptage': 3811255
}


i18n = {
    'de': {
        'default': {
            'weReceivedYourMsg': 'Wir haben deine Nachricht erhalten.',
            'thankYouForYourMsg': 'Vielen Dank für deine Nachricht.',
            'yourMsg': 'Deine Nachricht',
            'weTryContactYou': 'Wir versuchen dir innerhalb von 24 Stunden zu antworten.',
            'weReceivedAMsg': 'Wir haben eine neue Nachricht erhalten.',
            'newMsg': 'Neue Nachricht.',
            'theMsg': 'Die Nachricht',
            'from': 'Von'
        },
        'rollenspieltage2022': {
            'weReceivedYourMsg': 'Wir haben deine Anmeldung erhalten.',
            'thankYouForYourMsg': 'Vielen Dank für deine Anmeldung.',
            'yourMsg': 'Passe deine Anmeldung an',
            'weTryContactYou': 'Zögere nicht, uns bei Fragen oder Unklarheiten zu kontaktieren.',
            'weReceivedAMsg': 'Wir haben eine neue Anmeldung erhalten.',
            'newMsg': 'Neue Anmeldung.',
            'theMsg': 'Zur Anmeldung',
            'from': 'Von'
        }
    },
    'en': {
        'default': {
            'weReceivedYourMsg': 'We have received your message.',
            'thankYouForYourMsg': 'Thank you for your message.',
            'yourMsg': 'Your message',
            'weTryContactYou': 'We try replying within 24 hours to your message.',
            'weReceivedAMsg': 'We received a new message.',
            'newMsg': 'New message.',
            'theMsg': 'The message',
            'from': 'From'
        },
        'rollenspieltage2022': {
            'weReceivedYourMsg': 'We have received your registration.',
            'thankYouForYourMsg': 'Thank you for your registration.',
            'yourMsg': 'Adapt your registration',
            'weTryContactYou': 'Do not hesitate to contact us with any questions.',
            'weReceivedAMsg': 'We received a new registration.',
            'newMsg': 'New registration.',
            'theMsg': 'To the registration',
            'from': 'Von'
        }
    },
}


def config(public_key, private_key, version):
    return Client(auth=(public_key, private_key), version=version)


def mail_send(client, message, sender, recipient, template, language='de', kind='default', sendOnlyToUs=False):
    texts = i18n[language][kind]
    senderMail = sender.get('email')
    senderName = sender.get('name')

    copyToSender = {
        'To': [
            {
                'Email': senderMail,
                'Name': senderName
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
    }

    messageToRecipient = {
        'To': [
            {
                'Email': recipient['email'],
                'Name': recipient['name']
            }
        ],
        'TemplateID': mail_template.get(template),
        'TemplateLanguage': True,
        'Subject': texts['weReceivedAMsg'],
        'Variables': {
            'title': texts['newMsg'],
            'msgBeforeQuote': texts['theMsg'] + ':',
            'quote': message,
            'msgAfterQuote': texts['from'] + ' ' + (senderName if isinstance(senderName, str) else '-name missing-') + ', ' + (senderMail if isinstance(senderMail, str) else '-email missing-')
        }
    }

    if (senderMail is not None and senderName is not None):
        messageToRecipient['ReplyTo'] = {
            'Email': senderMail,
            'Name': senderName
        }

    data = {
        'Messages': [
            messageToRecipient
        ]
    }

    if (senderMail is not None and senderName is not None and not sendOnlyToUs):
        data['Messages'].append(copyToSender)

    client.send.create(data=data)
