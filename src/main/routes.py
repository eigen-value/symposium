from flask import request, render_template, jsonify
from flask_login import current_user
import json
from src import db
from src.main import bp
from src.models import *
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