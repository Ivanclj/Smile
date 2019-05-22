"""
Created on 5/10/19

@author: ivan chen

"""

import pandas as pd

def download_data(read_path,save_path):
    df = pd.read_csv(read_path,index_col=0)
    df.to_csv(save_path)


if __name__ == "__main__":
    url = 'https://raw.githubusercontent.com/Ivanclj/proj_data/master/survey.csv'
    download_data(url,"../data/survey.csv")

