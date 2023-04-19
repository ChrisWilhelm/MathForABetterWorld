### include functions that plot a graph in the given streamlit column
from collections import defaultdict

import streamlit as st
import datetime
import numpy as np
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import pandas as pd
import random as random
import json
from routeConnectors import pallet, exportConnectors
from matplotlib import pyplot as plt, dates as mdates
from routeConnectors import pallet
import json



# example:
def test(col):
    last_rows = np.random.randn(1, 1)
    # chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        last_rows = new_rows
    
    col.line_chart(last_rows)



def importGraph1(col):
    allPallets = json.loads(pallet.getFood())["Pallet"]

    df = pd.DataFrame.from_dict(allPallets)
    df = df.groupby('inputDate').agg(np.sum)

    df = df[['weight']]
    fig = plt.figure()
    fig.patch.set_facecolor('black')
    fig.patch.set_alpha(0.7)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    ax.set_title("Total imports over time")

    ax.plot(df.index, df[["weight"]], label="Daily Imports")
    ax.patch.set_facecolor('black')

    ax.legend()
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', colors='white')

    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Imports (lbs)")
    col.pyplot(fig)

def importGraph3(col):
    # TODO

    pallets = json.loads(pallet.getFood())
    Imports = pd.DataFrame(pallets["Pallet"])
    food_provider = Imports["companyId"].dropna().tolist()
    food_provider = set(food_provider)
    food_provider = defaultdict(float)
    for index, row in Imports.iterrows():
        food_provider[row['company']["name"]] += row['weight']

    provider_labels = []
    provider_sizes = []

    sorted_provider_labels = []
    sorted_provider_sizes = []

    for x, y in food_provider.items():
        provider_labels.append(x)
        provider_sizes.append(y)

    sorted_food_provider = sorted(food_provider.items(), key=lambda x: x[1])

    for x, y in dict(sorted_food_provider[-10:]).items():
        sorted_provider_labels.append(x)
        sorted_provider_sizes.append(y)

    sorted_other_labels = []
    sorted_other_providers = []

    for x, y in dict(sorted_food_provider[:-10]).items():
        sorted_other_labels.append(x)
        sorted_other_providers.append(y)

    other_total = sum(sorted_other_providers)

    sorted_provider_sizes.append(other_total)
    sorted_provider_labels.append("other")

    ImpTot = sum(sorted_provider_sizes)

    percTot = []
    for size in sorted_provider_sizes:
        perc = size / ImpTot * 100
        percTot.append(perc)

    for i in range(len(sorted_provider_labels)):
        sorted_provider_labels[i] = f'{sorted_provider_labels[i]}: {(float(percTot[i])):.1f}%'

    fig1, ax = plt.subplots()
    ax.pie(sorted_provider_sizes, labels=sorted_provider_labels)
    # plt.legend(provider_labels[-5:], bbox_to_anchor=(0,-2.7), loc="lower right")
    Imports_df = pd.DataFrame(list(zip(sorted_provider_sizes, sorted_provider_labels)),
                              columns=['Provider Imports', 'Provider'])

    col.bar_chart(data=Imports_df, x="Provider", y="Provider Imports", use_container_width=True)
    pass

def importGraph4(col):
    # TODO
    pallets = (pallet.getFood())
    exportItems = json.loads(exportConnectors.getExports())
    Exports = pd.DataFrame(exportItems["exports"])


    pallet_weights = Exports["weight"].dropna().values.tolist()

    food_receiver = defaultdict(float)

    for index, row in Exports.iterrows():
        food_receiver[row['category']["name"]] += np.absolute(row['weight'])

    receiver_labels = []
    receiver_sizes = []

    sorted_receiver_labels = []
    sorted_receiver_sizes = []

    for x, y in food_receiver.items():
        receiver_labels.append(x)
        receiver_sizes.append(y)

    sorted_food_receiver = sorted(food_receiver.items(), key=lambda x: x[1])


    for x, y in dict(sorted_food_receiver[-10:]).items():
        sorted_receiver_labels.append(x)
        sorted_receiver_sizes.append(y)

    sorted_other_rec_labels = []
    sorted_other_receivers = []

    for x, y in dict(sorted_food_receiver[:-10]).items():
        sorted_other_rec_labels.append(x)
        sorted_other_receivers.append(y)

    other_rec_total = sum(sorted_other_receivers)

    sorted_receiver_sizes.append(other_rec_total)
    sorted_receiver_labels.append("other")

    ItemExpTot = sum(sorted_receiver_sizes)
    receiverPercTot = []
    for size in sorted_receiver_sizes:
        receiverPerc = size / ItemExpTot * 100
        receiverPercTot.append(receiverPerc)

    for i in range(len(sorted_receiver_labels)):
        sorted_receiver_labels[i] = f'{sorted_receiver_labels[i]}: {(float(receiverPercTot[i])):.1f}%'
    Exports_df = pd.DataFrame(list(zip(sorted_receiver_sizes, sorted_receiver_labels)),
                              columns=['Quantity (lbs)', 'Item'])

    col.bar_chart(data=Exports_df, x="Item", y="Quantity (lbs)", use_container_width=True)

    pass

def importGraph2(col):
    allPallets = json.loads(pallet.getFood())["Pallet"]

    df = pd.DataFrame.from_dict(allPallets)
    df = df.groupby('inputDate').agg(np.sum)

    df = df[['weight']]
    totImports = np.cumsum(df)

    fig = plt.figure()
    fig.patch.set_facecolor('black')
    fig.patch.set_alpha(0.7)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    ax.set_title("Total imports over time")

    ax.plot(df.index, totImports, label="Cumulative Imports")
    ax.patch.set_facecolor('black')

    ax.legend()
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', colors='white')

    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Imports (lbs)")
    col.pyplot(fig)

    pass



def volunteerGraph1(col):
    a = datetime.datetime.today()
    numdays = 100
    dateList = []
    for x in range (0, numdays):
        dateList.append(a - datetime.timedelta(days = x))
    #dateList
    start = datetime.datetime.strptime("21-06-2014", "%d-%m-%Y")
    start = datetime.datetime.strptime("01-01-2023", "%d-%m-%Y")
    #now = datetime.datetime.today() # current date and time
    now = datetime.datetime.strptime("31-12-2023", "%d-%m-%Y")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    date_time = now.strftime("%m-%d-%Y")
    end = datetime.datetime.strptime(date_time, "%m-%d-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    dates = []
    for date in date_generated:
        dates.append(date.strftime("%d-%m-%Y"))
    
    volunteers_dates = []
    for i in range(len(dates)):
        volunteers_dates.append([dates[i], random.randint(1, 20)])
    df = pd.DataFrame(volunteers_dates, columns=['Date', 'Volunteers'])
    x = list(df.Date[-1:-8:-1])
    x.reverse()
    y = list(df.Volunteers[-1:-8:-1])
    y.reverse()
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    # actual graph::
    ax = plt.gca()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    fig.patch.set_alpha(0.7)
    ax.patch.set_facecolor('black')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', colors='white')
    fig.suptitle("Trend of Volunteers in the last Seven Days", color="white")
    ax.plot(x, y)
    ax.set_xlabel("Last Seven Days")
    ax.set_ylabel("Total Volunteer Hours per Day")
    col.pyplot(fig)

def volunteerGraph2(col):
    a = datetime.datetime.today()
    numdays = 100
    dateList = []
    for x in range (0, numdays):
        dateList.append(a - datetime.timedelta(days = x))
    #dateList
    start = datetime.datetime.strptime("21-06-2014", "%d-%m-%Y")
    start = datetime.datetime.strptime("01-01-2023", "%d-%m-%Y")
    #now = datetime.datetime.today() # current date and time
    now = datetime.datetime.strptime("31-12-2023", "%d-%m-%Y")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    date_time = now.strftime("%m-%d-%Y")
    end = datetime.datetime.strptime(date_time, "%m-%d-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    dates = []
    for date in date_generated:
        dates.append(date.strftime("%d-%m-%Y"))
    
    volunteers_dates = []
    for i in range(len(dates)):
        volunteers_dates.append([dates[i], random.randint(1, 20)])
    df = pd.DataFrame(volunteers_dates, columns=['Date', 'Volunteers'])
    x = list(df.Date[-1:-8:-1])
    x.reverse()
    y = list(df.Volunteers[-1:-8:-1])
    y.reverse()
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True


    volunteer_data = list(df.Volunteers)
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    sd = 0
    month_average = []
    volunteer = []
    for mindex, m in enumerate(months):
        #print(type(m))
        sum_data = 0
        for dindex, d in enumerate(dates):
            #print(dindex)
            if df.Date[dindex].find(m,3,5) != -1:
                sum_data = sum_data + df.Volunteers[dindex]
        volunteer.append(sum_data)
    
    # actual graph::
    fig2, ax2 = plt.subplots()
    fig2.patch.set_facecolor('black')
    fig2.patch.set_alpha(0.7)
    ax2.patch.set_facecolor('black')
    ax2.xaxis.label.set_color('white')
    ax2.yaxis.label.set_color('white')
    ax2.tick_params(axis='y', colors='white')
    ax2.tick_params(axis='x', colors='white')
    ax2.plot(months, volunteer)
    ax2.set_xlabel("Months")
    ax2.set_ylabel("Total Volunteer Hours")
    fig2.suptitle("Trend of Total Volunteers in the last 12 months", color="white")
    col.write(fig2)

def volunteerGraph3(col):
    # TODO
    test(col)
    pass

def volunteerGraph4(col):
    # TODO
    test(col)
    pass



def clientGraph1(col):
    # TODO
    test(col)
    pass

def clientGraph2(col):
    # TODO
    test(col)
    pass

def clientGraph3(col):
    # TODO
    test(col)
    pass

def clientGraph4(col):
    # TODO
    test(col)
    pass



def distributorGraph1(col):
    # TODO
    test(col)
    pass

def distributorGraph2(col):
    # TODO
    test(col)
    pass

def distributorGraph3(col):
    # TODO
    test(col)
    pass

def distributorGraph4(col):
    # TODO
    test(col)
    pass



def tempImportLineGraph():
    last_rows = np.random.randn(1, 1)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        last_rows = new_rows

    return st.line_chart(last_rows)

def tempDistributorsBarGraph(key):
    last_rows = np.random.randn(1, 1)
    # chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        last_rows = new_rows

    return st.bar_chart(last_rows)

def tempVolunteerVis(col):
    a = datetime.datetime.today()
    numdays = 100
    dateList = []
    for x in range (0, numdays):
        dateList.append(a - datetime.timedelta(days = x))
    start = datetime.datetime.strptime("01-01-2023", "%d-%m-%Y")
    now = datetime.datetime.strptime("31-12-2023", "%d-%m-%Y")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    date_time = now.strftime("%m-%d-%Y")
    end = datetime.datetime.strptime(date_time, "%m-%d-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    dates = []
    for date in date_generated:
        dates.append(date.strftime("%d-%m-%Y"))

    volunteers_dates = []
    for i in range(len(dates)):
        volunteers_dates.append([dates[i], random.randint(1, 20)])
        
    df = pd.DataFrame(volunteers_dates, columns=['Date', 'Volunteers'])

    x = list(df.Date[-1:-8:-1])
    x.reverse()
    y = list(df.Volunteers[-1:-8:-1])
    y.reverse()

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    ax = plt.gca()
    fig, ax = plt.subplots()


    ax.set_title("Trend of Volunteers in the last Seven Days")
    ax.plot(x, y)
    ax.set_xlabel("Last Seven Days")
    ax.set_ylabel("Total Volunteer Hours per Day")
    col.pyplot(fig)

def tempImportVis(col):
    a = datetime.datetime.today()
    numdays = 100
    dateList = []
    for x in range (0, numdays):
        dateList.append(a - datetime.timedelta(days = x))
    start = datetime.datetime.strptime("01-01-2023", "%d-%m-%Y")
    now = datetime.datetime.strptime("31-12-2023", "%d-%m-%Y")
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    date_time = now.strftime("%m-%d-%Y")
    end = datetime.datetime.strptime(date_time, "%m-%d-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    dates = []
    for date in date_generated:
        dates.append(date.strftime("%d-%m-%Y"))

    volunteers_dates = []
    for i in range(len(dates)):
        volunteers_dates.append([dates[i], random.randint(1, 20)])
        
    df = pd.DataFrame(volunteers_dates, columns=['Date', 'Volunteers'])

    x = list(df.Date[-1:-8:-1])
    x.reverse()
    y = list(df.Volunteers[-1:-8:-1])
    y.reverse()
    y = np.cumsum(y)

    m = max(y) + 10
    mx = [m for i in range(len(y))]

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    ax = plt.gca()
    fig, ax = plt.subplots()


    ax.set_title("Total imports over time")
    ax.plot(x, y, label="Cumulative Imports")
    ax.plot(x, mx, label="Goal")
    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Cumulative Imports (lbs)")
    col.pyplot(fig)