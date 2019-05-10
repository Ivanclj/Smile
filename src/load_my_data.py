"""
Created on 5/10/19

@author: ivanchen

"""

import pandas as pd

url = 'https://raw.githubusercontent.com/pydata/pydata-book/master/ch09/stock_px.csv'
df = pd.read_csv(url,index_col=0,parse_dates=[0])

print df.head(5)