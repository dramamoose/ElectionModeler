import pandas as pd


data = pd.read_csv('https://raw.githubusercontent.com/dramamoose/ElectionModeler/master/resources/538Data.csv', index_col=0)
d = data.transpose().to_dict(orient='series')