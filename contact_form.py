from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email

class ContactForm(FlaskForm):
    full_name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    message = StringField('Message', validators=[DataRequired()])