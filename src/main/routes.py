from flask import request, render_template, jsonify, flash, redirect, url_for
from flask_login import current_user
import json
from src import db
from src.main import bp
from src.main.forms import SubscriptionForm
from src.models import *
from src.main.email import send_subscription_confirmation_email
from config.default import basedir


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/home')
def home():
    return render_template("home.html", navbar=True, side_index=True)


@bp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():

    form = SubscriptionForm()
    if form.validate_on_submit():
        participant = Participant(title=form.title.data, name=form.name.data, surname=form.surname.data,
                                  institution=form.institution.data, email=form.email.data)

        db.session.add(participant)
        db.session.commit()
        flash('Iscrizione effettuata con successo')
        send_subscription_confirmation_email(participant=participant)
        return redirect(url_for('main.home'))
    else:
        participant = Participant.query.filter_by(email=form.email.data).first()
        if participant is not None:
            flash("Indirizzo e-mail già presente. Se non si è ricevuta la notifica di avvenuta iscrizione si prega di contattare l'organizzazione")
    return render_template('subscribe.html', title='Subscribe', form=form)
