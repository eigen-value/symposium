from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from src.models import Participant, ParticipantTitle


class SubscriptionForm(FlaskForm):
    title = SelectField('Titolo', choices=[(name_, member.value)     # name_.capitalize() can be used if enum names are to be shown
                                           for name_, member in ParticipantTitle.__members__.items()])
    name = StringField('Nome', validators=[DataRequired()])
    surname = StringField('Cognome', validators=[DataRequired()])
    institution = StringField('Affiliazione', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Iscriviti')

    def validate_email(self, email):
        user = Participant.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Indirizzo Email già presente.')