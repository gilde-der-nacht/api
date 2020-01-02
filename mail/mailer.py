#!/usr/bin/env python3

import json

from flask_mail import Mail, Message

# see https://pythonhosted.org/Flask-Mail/ for E-Mail configuration
MAIL_SENDER = 'mail@gildedernacht.ch'
MAIL_RECIPIENTS = ['mail@gildedernacht.ch']
MAIL_SUBJECT_PREFIX = 'Mail from Olymp: '
EMAIL_DISABLED = False
NEW_LINE = '\r\n'
DOUBLE_NEW_LINE = NEW_LINE + NEW_LINE


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
                lines += key2 + ':' + NEW_LINE + str(value2) + DOUBLE_NEW_LINE
        else:
            lines += key + ':' + NEW_LINE + value + DOUBLE_NEW_LINE

    return lines


def mail_send(mail, subject, body, recipients):
    body_formatted = body_formatting(body) + DOUBLE_NEW_LINE + str(body)
    if EMAIL_DISABLED:
        return
    recipients = recipients if recipients else MAIL_RECIPIENTS
    msg = Message(subject=MAIL_SUBJECT_PREFIX + subject,
                  body=body_formatted,
                  sender=MAIL_SENDER,
                  recipients=recipients)
    mail.send(msg)
