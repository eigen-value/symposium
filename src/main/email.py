from flask import render_template, current_app
from src.email_utils import send_email


def send_subscription_confirmation_email(participant):
    send_email('{}: {} - Iscrizione effettuata'.format(current_app.config['EMAIL_SENDER_TEXT'],
                                                       current_app.config['CONFERENCE_NAME']),
               sender=current_app.config['ADMINS'][0],
               recipients=[participant.email],
               text_body=render_template('email/subscription_confirmation.txt',
                                         participant=participant),
               html_body=render_template('email/subscription_confirmation.html',
                                         participant=participant))
