from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, ValidationError


def name_validation(form, field):
    if len(field.data) > 50:
        raise ValidationError('Name must be less than 50 characters.')
    elif len(field.data) < 2:
        raise ValidationError('Name is too short.')


def email_validation(form, field):
    if len(field.data) > 100:
        raise ValidationError('Email must contain less than 100 characters.')


def message_validation(form, field):
    if len(field.data) < 5:
        raise ValidationError('Message is too short.')
    elif len(field.data) > 1000:
        raise ValidationError('Message can NOT be longer than 1000 characters.')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), name_validation])
    email = StringField('Email Address', validators=[DataRequired(), Email(granular_message=True), email_validation])
    message = TextAreaField('Message', validators=[DataRequired(), message_validation])
    submit = SubmitField('Submit')

