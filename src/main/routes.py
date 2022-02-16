from flask import request, render_template, jsonify, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
import uuid
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
        #filename = secure_filename(form.receipt.data.filename)
        filename = uuid.uuid4().hex + 'receipt.pdf'
        receipts_path = os.path.join(current_app.root_path, 'static', 'receipts')
        if not os.path.isdir(receipts_path):
            os.mkdir(receipts_path)
        form.receipt.data.save(os.path.join(receipts_path, filename))

        receipt_location = '/'.join(['static', 'receipts', filename])
        participant = Participant(title=form.title.data, name=form.name.data, surname=form.surname.data,
                                  institution=form.institution.data, email=form.email.data,
                                  needs_accommodation=form.needs_accommodation.data,
                                  chosen_accommodation_id=form.chosen_accommodation.data,
                                  receipt_location=receipt_location)

        db.session.add(participant)
        db.session.commit()
        send_subscription_confirmation_email(participant=participant)
        flash('Iscrizione effettuata con successo', 'success')
        return redirect(url_for('main.home'))
    else:
        participant = Participant.query.filter_by(email=form.email.data).first()
        if participant is not None:
            flash("Indirizzo e-mail già presente.", 'warning')
    return render_template('subscribe.html', title='Subscribe', form=form)

@bp.route('/accommodations', methods=['GET'])
def accommodations():

    accommodations = Accommodation.query.all()
    return render_template('accommodations.html', accommodations=accommodations)

