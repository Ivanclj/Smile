"""
Created on 6/6/19

@author: ivanchen

"""

"""
Created on 6/6/19

@author: ivanchen

"""


import os
import pandas as pd
from Smile.src.evaluate_model import evalClassModel
import warnings
warnings.filterwarnings("ignore")
import yaml
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def test_evalClassModel():
    with open('config/config.yml', "r") as f:
        config = yaml.load(f)

    config = config['evaluate_model']
    path = config['path_to_tmo']
    with open(path, 'rb') as output:
        forest = pickle.load(output)
        print('model loaded successfully')

    ##load test set
    X = pd.read_csv(config['dataset']['X'], index_col=0)
    y = pd.read_csv(config['dataset']['y'], index_col=0)
    y = y['treatment']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config['split_data']['test_size'],
                                                        random_state= int(config['split_data']['random_state']))



    # make class predictions for the testing set
    y_pred_class = forest.predict(X_test)

    accuracy_score = evalClassModel(X,y,forest, y_test, y_pred_class, True)

    assert round(accuracy_score,2) == 0.74
