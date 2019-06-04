"""
Created on 5/27/19

@author: ivanchen

"""

import os
import pandas as pd
from Smile.src.generate_features import clean_data

def test_clean_data():
    my_df = pd.read_csv('data/survey.csv', index_col=0).reset_index()

    my_df = clean_data(my_df)

    row = 1158
    columns = 43
    assert row == my_df.shape[0]
    assert columns == my_df.shape[1]