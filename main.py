from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt

pastyearflag = 0
targeturl = 'https://www.realclearpolitics.com/epolls/other/president_trump_job_approval-6179.html'
targeturl1 = 'https://www.realclearpolitics.com/epolls/2016/senate/nh/new_hampshire_senate_ayotte_vs_hassan-3862.html'


def importdata(targeturl):
    print('Getting poll results from ', targeturl)
    response = urlopen(targeturl)
    metadata = {}


    soup = BeautifulSoup(response, 'html.parser')

    fp = soup.find("div", {"id": 'polling-data-full'})
    rows = fp.find('table', {"class": 'data'})
    print('Found ', len(rows), ' polls')

    p = []
    cleanedp = []
    for row in rows:
        cols = row.find_all(['th', 'td'])
        p.append([ele.text.strip() for ele in cols])
    headers = p.pop(0)
    headers.insert(len(headers), 'Start Date')
    headers.insert(len(headers), 'End Date')
    for row in range(0, len(p)):
        if p[row][0] != 'Final Results' and p[row][0] != 'RCP Average':
            dateinserts = convertdates(p[row][1])
            p[row].insert(len(p[row]), dateinserts[0])
            p[row].insert(len(p[row]), dateinserts[1])
            cleanedp.append(p[row])
    df = pd.DataFrame(cleanedp, columns=headers)
    #Specific Cleaning
    if headers[3] == 'Approve':
        print('This is an Approval Poll')
        df[['Approve', 'Disapprove', 'Spread']] = df[['Approve', 'Disapprove', 'Spread']].apply(pd.to_numeric, errors='coerce')
        df[['Spread']] = df[['Spread']].fillna(0)
    else:
        spliturl = targeturl.split('/')
        metadata["year"] = spliturl[4]
        metadata["category"] = spliturl[5]
        metadata["state"] = spliturl[6]
        print('These polls are from the',metadata["year"], metadata["state"], metadata["category"], "race.")
        df[[headers[3], headers[4]]] = df[[headers[3], headers[4]]].apply(pd.to_numeric, errors='coerce')

    return df, metadata


def convertdates(daterange):
    datestring = daterange.replace(" ", "")
    cleandates = datestring.split('-')
    currentmonth = date.today().month
    currentday = date.today().day
    global pastyearflag
    finaldates = []
    for dateposition in range(0, len(cleandates)):
        finaldates.insert(dateposition,datetime.strptime(cleandates[dateposition], '%m/%d'))
        if pastyearflag == 1:
            finaldates[dateposition] = finaldates[dateposition].replace(year=date.today().year - 1)
        elif finaldates[dateposition].month > currentmonth:
            finaldates[dateposition] = finaldates[dateposition].replace(year=date.today().year - 1)
        else:
            finaldates[dateposition] = finaldates[dateposition].replace(year = date.today().year)
        if dateposition == 1 and (finaldates[dateposition].year != date.today().year):
            pastyearflag = 1

    return finaldates
def plothistogram(data, title = 'Histogram'):
    hist, bins = np.histogram(data, bins='auto')
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.title(title)
    plt.show()

polldata, pollmeta = importdata(targeturl1)
