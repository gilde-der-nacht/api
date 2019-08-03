#!/usr/bin/env python3

from flask_mail import Mail, Message

# see https://pythonhosted.org/Flask-Mail/ for E-Mail configuration
MAIL_SENDER = 'mail@gildedernacht.ch'
MAIL_RECIPIENTS = ['mail@rollenspieltage.ch']
MAIL_SUBJECT_PREFIX = 'Mail from Olymp: '
EMAIL_DISABLED = False


def mail_config(app):
    app.config['MAIL_PORT'] = 2500  # mailslurper uses port 2500 as default
    mail = Mail(app)
    return mail


def mail_send(mail, subject, body):
    if EMAIL_DISABLED:
        return
    msg = Message(subject=MAIL_SUBJECT_PREFIX + subject,
                  body=body,
                  sender=MAIL_SENDER,
                  recipients=MAIL_RECIPIENTS)
    mail.send(msg)
