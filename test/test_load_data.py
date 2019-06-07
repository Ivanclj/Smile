"""
Created on 5/21/19

@author: ivanchen

"""
import os
import pandas as pd
from Smile.src.load_data import download_data

def test_download_data():
    url = 'https://raw.githubusercontent.com/Ivanclj/proj_data/master/survey.csv'
    test_df = download_data(url)
    row = 1259
    columns = 26


    assert test_df is not None
    assert row == test_df.shape[0]
    assert columns == test_df.shape[1]



