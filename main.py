from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from datetime import datetime
import requests
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

how_old_am_i = datetime.today().year - datetime.strptime('March 1, 2001', '%B %d, %Y').year


# Pass current_year variable to all HTML templates
@app.context_processor
def inject_current_year():
    return dict(current_year=datetime.today().year, how_old_am_i=how_old_am_i)


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


if __name__ == '__main__':
    app.run(debug=False)
