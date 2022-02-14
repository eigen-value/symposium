from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
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
    receipt = FileField('Caricare qui la ricevuta del versamento', validators=[FileRequired(), FileAllowed(['pdf'], "Solo file pdf")])
    submit = SubmitField('Iscriviti')
    recaptcha = RecaptchaField()

    def validate_email(self, email):
        participant = Participant.query.filter_by(email=email.data).first()
        if participant is not None:
            raise ValidationError('Indirizzo Email già presente.')