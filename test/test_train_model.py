"""
Created on 6/6/19

@author: ivanchen

"""


import os
import pandas as pd
from Smile.src.train_model import split_data,randomForest
import warnings
warnings.filterwarnings("ignore")
import yaml
import pickle
from sklearn.ensemble import RandomForestClassifier


def test_split_data():
    with open("config/config.yml", "r") as f:
        config = yaml.load(f)

    config = config['train_model']

    X = pd.read_csv(config['data']['X'], index_col=0)
    y = pd.read_csv(config['data']['y'], index_col=0)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=config['split_data']['test_size'],
                                                        random_state=config['split_data']['random_state'])

    row = 926
    columns = 8
    assert row == X_train.shape[0]
    assert columns == X_train.shape[1]

def test_randomForest():

    with open("config/config.yml", "r") as f:
        config = yaml.load(f)

    config = config['train_model']
    path = config['save_tmo']
    with open(path, 'rb') as output:
        forest = pickle.load(output)
        print('model loaded successfully')

    forest_test = RandomForestClassifier(n_estimators=10)
    assert type(forest)==type(forest_test)

