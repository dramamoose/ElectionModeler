import pandas as pd


mastercsv = pd.read_csv('https://raw.githubusercontent.com/dramamoose/ElectionModeler/master/resources/538Data.csv', index_col=0)
csvdict = mastercsv.to_dict()
polldata = {}
for polls in csvdict['URL']:
    print('Pulling entry', polls, 'from', csvdict['URL'][polls])
    polldata[polls] = pd.read_csv(csvdict['URL'][polls])
    polldata[polls]['enddate'] = pd.to_datetime(polldata[polls]['enddate'])
    polldata[polls]['startdate'] = pd.to_datetime(polldata[polls]['startdate'])
    polldata[polls]['modeldate'] = pd.to_datetime(polldata[polls]['modeldate'])
    polldata[polls]['createddate'] = pd.to_datetime(polldata[polls]['createddate'])
    polldata[polls]['timestamp'] = pd.to_datetime(polldata[polls]['timestamp'])