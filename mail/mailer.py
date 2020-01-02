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


# def body_formatting(body):
#     lines = []
#     for key, value in json.loads(body):
#         lines.append(key + ': ' + value + '\n')
#
#     lines.append('\n\n' + body)
#     return json.dumps(lines)


def mail_send(mail, subject, body):
    # body = body_formatting(body);
    if EMAIL_DISABLED:
        return
    msg = Message(subject=MAIL_SUBJECT_PREFIX + subject,
                  body=body,
                  sender=MAIL_SENDER,
                  recipients=MAIL_RECIPIENTS)
    mail.send(msg)
