
import traceback
from flask import render_template, request, redirect, url_for
import logging.config
# from app.models import Tracks
from flask import Flask
from src.database import User_Prediction
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("Ivan")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        #tracks = db.session.query(User_Prediction).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        return render_template('index.html')#, tracks=tracks)
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """

    try:
        track1 = User_Prediction(
                                 age = request.form['age'],
                                 gender=request.form['gender'],
                                 country=request.form['country'],
                                 states=request.form['states'],
                                 benefits=request.form['benefits'],
                                 care_options=request.form['care_options'],
                                 leave=request.form['leave'],
                                 coworksers=request.form['coworksers'],
                                 family_history=request.form['family_history'],
                                 no_employees=request.form['no_employees'],
                                 predicted_score=request.form['predicted_score'],
                                 )
        db.session.add(track1)
        db.session.commit()
        logger.info("New song added: %s by %s", request.form['ip'], request.form['age'])
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')
