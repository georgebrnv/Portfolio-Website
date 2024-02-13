from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests
from contact_form import ContactForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Git REST API setup
GIT_USER = 'georgebrnv'
URL = f'https://api.github.com/users/{GIT_USER}/repos'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_APP_KEY')
Bootstrap5(app)

# SMTPLIB email
MY_EMAIL = "egor.barinov.us@gmail.com"
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASS')

# Load environment variables from .env file
load_dotenv()


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
            # Sent email
            sent_email_message(name=name, email=email, message=message)
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


def sent_email_message(name, email, message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=GMAIL_APP_PASSWORD)
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
        message = MIMEMultipart()
        message['Subject'] = 'Portfolio Website Contact Form'
        message['From'] = MY_EMAIL
        message['To'] = MY_EMAIL
        message.attach(MIMEText(html, 'html'))
        message.attach(MIMEText(text, 'plain'))

        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=message.as_string())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
