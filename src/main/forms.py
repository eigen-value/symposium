from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from src.models import Participant, ParticipantTitle, Accommodation


class SubscriptionForm(FlaskForm):
    title = SelectField('Titolo', choices=[(name_, member.value)     # name_.capitalize() can be used if enum names are to be shown
                                           for name_, member in ParticipantTitle.__members__.items()])
    name = StringField('Nome', validators=[DataRequired()])
    surname = StringField('Cognome', validators=[DataRequired()])
    institution = StringField('Affiliazione', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    needs_accommodation = BooleanField('Prenotazione alberghiera')
    chosen_accommodation = SelectField('Struttura scelta')
    receipt = FileField('Caricare qui la ricevuta del versamento', validators=[FileRequired(), FileAllowed(['pdf'], "Solo file pdf")])
    submit = SubmitField('Iscriviti')
    recaptcha = RecaptchaField()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chosen_accommodation.choices = [('', '')] + [(c.id, c.name) for c in Accommodation.query.all()]

    def validate_email(self, email):
        participant = Participant.query.filter_by(email=email.data).first()
        if participant is not None:
            raise ValidationError('Indirizzo Email già presente.  Se non si è ricevuta la notifica di avvenuta iscrizione si prega di contattare l\'organizzazione')