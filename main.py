from flask import Flask, abort, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "egor.barinov123"
Bootstrap5(app)


# Pass current_year variable to all HTML templates
@app.context_processor
def inject_current_year():
    return dict(current_year=datetime.today().year)


@app.route('/', methods=['GET', 'POST'])
def home():
    current_year = datetime.today().year
    return render_template('index.html')


@app.route('/resume', methods=['GET', 'POST'])
def resume():
    return render_template('resume.html')


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    return render_template('projects.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
