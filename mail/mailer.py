#!/usr/bin/env python3

import json
from flask_mail import Mail, Message

# see https://pythonhosted.org/Flask-Mail/ for E-Mail configuration
MAIL_SENDER = 'mail@gildedernacht.ch'
MAIL_RECIPIENTS = ['mail@gildedernacht.ch']
MAIL_SUBJECT_PREFIX = 'Mail from Olymp: '
EMAIL_DISABLED = False


def mail_config(app, host, username, password):
    app.config['MAIL_SERVER'] = host
    app.config['MAIL_USERNAME'] = username
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = True
    mail = Mail(app)
    return mail


def body_formatting(body):
    lines = ''
    body = json.loads(body)

    for key, value in body.items():
        if key.endswith('Body'):
            value = json.loads(value)
            for key2, value2 in value.items():
                lines += key2 + ': ' + str(value2) + '\n'
        else:
            lines += key + ': ' + value + '\n'

    return lines


def mail_send(mail, subject, body):
    NEW_LINE = '\r\n'
    body_formatted = body_formatting(body) + NEW_LINE + NEW_LINE + str(body)
    if EMAIL_DISABLED:
        return
    msg = Message(subject=MAIL_SUBJECT_PREFIX + subject,
                  body=body_formatted,
                  sender=MAIL_SENDER,
                  recipients=MAIL_RECIPIENTS)
    mail.send(msg)
