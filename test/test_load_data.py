"""
Created on 5/21/19

@author: ivanchen

"""
import os
import pandas as pd
from Smile.src.load_my_data import download_data

def test_download_data():
    url = 'https://raw.githubusercontent.com/Ivanclj/proj_data/master/survey.csv'
    download_data(url,"survey.csv")
    row = 1259
    columns = 26

    data = pd.read_csv("survey.csv",index_col=0)
    os.system('rm survey.csv')

    assert data is not None
    assert row == data.shape[0]
    assert columns == data.shape[1]



