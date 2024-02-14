from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests
from contact_form import ContactForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Git REST API setup
GIT_USER = 'georgebrnv'
URL = f'https://api.github.com/users/{GIT_USER}/repos'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_APP_KEY')
Bootstrap5(app)

# SMTPLIB email
MY_EMAIL = "egor.barinov.us@gmail.com"
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASS')


# Pass current_year variable to all HTML templates
@app.context_processor
def inject_current_year():
    return dict(current_year=datetime.today().year)


@app.route('/', methods=['GET', 'POST'])
def home():
    git_response = requests.get(url=URL)
    data = git_response.json()
    # Sort data by "last time updated" and take last 6 projects.
    sorted_data = sorted(data, key=lambda x: x["updated_at"], reverse=True)[:6]
    return render_template('index.html', git_projects_data=sorted_data)


@app.route('/resume', methods=['GET', 'POST'])
def resume():
    return render_template('resume.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data
            # MIMEText template
            html = f"""\
                        <html>
                        <head></head>
                        <body>
                        <h2 style="font-weight: bold;">Portfolio Website Contact Form</h2>
                        <p style="font-size: 20px"><strong>PROVIDED EMAIL:</strong> {email}</p>
                        <p style="font-size: 20px"><strong>PROVIDED NAME:</strong> {name}</p>
                        </body>
                        </html>
                    """
            text = message
            message_mime = MIMEMultipart()
            message_mime['Subject'] = 'Portfolio Website Contact Form'
            message_mime['From'] = MY_EMAIL
            message_mime['To'] = MY_EMAIL
            message_mime.attach(MIMEText(html, 'html'))
            message_mime.attach(MIMEText(text, 'plain'))
            # Sent email
            sent_email_message(message=message_mime)
            # Flash success message
            flash('Message was successfully sent.', 'success')
            return redirect(url_for('contact'))
        else:
            # Flash error messages from form errors dictionary
            flash_errors(form)
    return render_template('contact.html', form=form)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{error}", "warning")


def sent_email_message(message):
    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=GMAIL_APP_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=message.as_string())
            print('Email was successfully sent.')
    except Exception as e:
        print(f'Error sending email: {e}')


if __name__ == '__main__':
    app.run(debug=False)
