from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from src.models import User


class LoginForm(FlaskForm):
    username = StringField('Nome Utente', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Entra')


class RegistrationForm(FlaskForm):
    username = StringField('Nome Utente', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Ripeti Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Registrati')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Nome utente già presente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Indirizzo Email già presente.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reimposta password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Non è presente un utente con questo indirizzo email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Ripeti Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Invia Richiesta')
