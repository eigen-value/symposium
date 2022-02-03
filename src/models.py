import base64
import enum
import os
import jwt
from flask import current_app
from time import time
from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from src import db, login_manager
from datetime import datetime, timedelta

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True, nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=user_role, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256')  # .decode('utf-8') ? python 2.7

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return

    def is_super(self):
        return any(map(lambda r: r.type == RoleType.super, self.roles))

    def is_active(self):
        return bool(self.active)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class RoleType(enum.Enum):
    super = 10
    standard = 20


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    type = db.Column(Enum(RoleType))
    description = db.Column(db.String(1000))

    def __repr__(self):
        return '<Role> {}>'.format(self.name)


class ParticipantTitle(enum.Enum):
    none = "None"
    doctor = "Dr."
    professor = "Prof."


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(Enum(ParticipantTitle))
    name = db.Column(db.String(255), index=True, unique=True)
    surname = db.Column(db.String(255), index=True, unique=True)
    institution = db.Column(db.String(512), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Participant {} {}>'.format(self.name, self.surname)

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'name': self.name,
            'surname': self.surname,
            'institution': self.institution,
            'email': self.email,
        }

        return data