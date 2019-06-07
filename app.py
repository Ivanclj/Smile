#!/usr/bin/env python3
import traceback
from flask import render_template, request, redirect, url_for
import logging.config
# from app.models import Tracks
from flask import Flask
from src.database import User_Prediction
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pickle

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flask_config.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("Ivan")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
@app.route('/home',methods=['POST'])
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
        logger.warning("index page unable to load")
        return render_template('error.html')

@app.route('/predict', methods = ['POST','GET'])
def load_prediction():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        #tracks = db.session.query(User_Prediction).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("prediction page accessed")
        return render_template('prediction.html')#, tracks=tracks)
    except:
        traceback.print_exc()
        logger.warning("prediction page unable to load")
        return render_template('error.html')


@app.route('/contact',methods=['POST'])
def get_contact():
    try:
        #tracks = db.session.query(User_Prediction).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("contact page accessed")
        return render_template('contact.html')#, tracks=tracks)
    except:
        traceback.print_exc()
        logger.warning("contact page unable to load")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """


    try:


        # retrieve features
        logger.info("start retrieving!")
        age = request.form['age']
        #print(age)
        gender = request.form['gender']
        #print(gender)
        country = request.form['country']
        #print(country)
        try:
            states = request.form['states']
        except:
            states = "Null"
        benefits = request.form['Benefits']
        care_options = request.form['care_options']
        leave = request.form['leave']
        coworksers = request.form['coworksers']
        family_history = request.form['family_history']
        print(family_history)
        no_employees = request.form['no_employees']
        logger.info("all inputs retrieved!")

        # load trained model
        path_to_tmo = app.config["PATH_TO_MODEL"]
        with open(path_to_tmo, "rb") as f:
            model = pickle.load(f)
        logger.info("model loaded!")

        # create a dataframe to store inputs for prediction
        mydf = pd.DataFrame(columns=["Age","Gender","country","states","family_history",
                                         "no_employees","benefits",
                                         "care_options","leave","coworkers"])

        mydf.loc[0] = [age, gender, country, states, family_history,
                           no_employees, benefits, care_options,leave,coworksers]



        # change datatype from object to float
        pred_df = mydf[["Age","Gender","family_history",
                        "no_employees","benefits",
                        "care_options","leave","coworkers"]]





        pred_df = pred_df.apply(pd.to_numeric)
        print(pred_df)
        # make a prediction
        prob = model.predict_proba(pred_df)[:, 1][0]
        print('probability:%s'%prob)
        logger.info("prediction made: {:0.3f}".format(prob))

        if prob >= 0.8:
            evaluation = "Highly likely to suffer from mental problem"
        elif prob >= 0.5 and prob < 0.8:
            evaluation = "Potentially suffer from mental problem"
        elif prob >= 0.2 and prob < 0.5:
            evaluation = "Not very likely to suffer from mental problem"
        else:
            evaluation = "Unlikely to suffer from mental problem"

        #
        track1 = User_Prediction(
                                 age = age,
                                 gender=gender,
                                 country=country,
                                 states=states,
                                 benefits=benefits,
                                 care_options=care_options,
                                 leave=leave,
                                 coworksers=coworksers,
                                 family_history=family_history,
                                 no_employees=no_employees,
                                 predicted_score=float(prob),
                                 )
        db.session.add(track1)
        db.session.commit()
        return render_template('about.html',prob = float(round(prob*100,2)),results = evaluation)
    except BaseException as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        logger.warning("Not able to add entry, error page returned")
        return render_template('error.html')

@app.route('/error', methods=['GET'])
def get_error():
    return  render_template('error.html')

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])