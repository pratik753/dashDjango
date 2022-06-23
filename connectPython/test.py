# import sys
from tkinter.ttk import Style
import pandas as pd
# from connectPython.Filter_Page import custom_customer_trader_head
import numpy as np
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
#from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from jupyter_dash import JupyterDash  # pip install dash
#import dash_cytoscape as cyto
from dash.dependencies import Output, Input
import json


df = pd.read_excel(
    'https://github.com/pratik753/dashNew/raw/main/Book2.xlsx')
df.drop(df[df['Transaction Type'] == 'Deposit'].index, inplace=True)
df.reset_index(drop=True, inplace=True)
df_trade = pd.read_excel(
    'https://github.com/pratik753/dashNew/raw/main/Item_file_1.xlsx')
df_item = pd.read_excel(
    'https://github.com/pratik753/dashNew/raw/main/Trade_file_1.xlsx')
df_item.columns = ['Product/Service', 'Category']
df['day'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.day  # inegrate
df['Date_month'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.month
df['Date_year'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.year
df['Date_Month1'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.month
day = []  # inegrate
for i in range(len(df)):  # inegrate
    x1 = str(df['Date_year'][i])+'-'+str(df['Date_month'][i]) + \
        '-'+str(df['day'][i])  # inegrate
    day.append(x1)  # inegrate
df['day'] = day  # inegrate
df['Date_Month1'].replace({1: 'Jan', 2: 'Feb', 3: 'March', 4: 'Apr', 5: 'May', 6: 'June',
                          7: 'July', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}, inplace=True)  # inegrate
# df.drop(['Qty', 'Sales Price'], axis=1, inplace=True)  # inegrate
df_new = df.copy()  # inegrate


def changeP(x):
    if x >= 10e+6:
        x = round(x/10e+6, 3)
        x = str(x)+' Cr.'
    elif x < 10e+6 and x >= 10e+4:
        x = round(x/10e+4, 3)
        x = str(x)+' Lakhs.'
    elif x < 10e+4 and x >= 10e+2:
        x = round(x/10e+2, 3)
        x = str(x)+' K.'
    else:
        x = str(x)
    return x


def merge_file(original, merge1, on1):
    data1 = original.copy()
    data2 = merge1.copy()
    lst_cust = data1[on1].unique()
    customer = []
    for i in lst_cust:
        if i not in list(data2[on1].unique()):
            customer.append(i)
    col = list(merge1.columns)
    Trade = ['New_'+col[-1]+'_Head']*len(customer)
    df1 = pd.DataFrame()
    df1[on1] = customer
    df1[col[-1]] = Trade
    data2 = pd.concat([data2, df1], axis=0)
    data1 = pd.merge(data1, data2, on=on1)
    data1['Date'] = pd.to_datetime(data1['Date'], format="%d-%m-%Y")
    data1.sort_values('Date', ascending=True, inplace=True)
    data1.reset_index(inplace=True, drop=True)
    return data1


def past_VI_XII_month(data_1, axis, step=6, no_cust=2, data_2=df_trade):
    no_cust = str(no_cust)
    data1 = data_1.copy()
    data2 = data_2.copy()
    coln = list(data2.columns)
    data1 = merge_file(data1, data2, coln[0])
    mon_yr = []
    for i in range(len(data1)):
        x = str(data1['Date_month'][i])+'-'+str(data1['Date_year'][i])
        mon_yr.append(x)
    data1['Month_year'] = mon_yr
    month1 = dt.datetime.now().month
    year1 = dt.datetime.now().year
    if (str(month1)+'-'+str(year1)) not in (data1['Month_year'].unique()):
        month1 = data1['Date_month'][len(data1)-1]
        year1 = data1['Date_year'][len(data1)-1]
    month2 = month1 - step + 1
    year2 = dt.datetime.now().year
    if month2 <= 0:
        month2 = 12+month2
        year2 = year1-1
    if ((str(month2)+'-'+str(year2)) not in list(data1['Month_year'].unique())):
        month2 = data1['Date_month'][0]
        year2 = data1['Date_year'][0]
    fin1 = (str(month1)+'-'+str(year1))
    ini1 = (str(month2)+'-'+str(year2))
    mon_yr1 = []
    for i in range(len(data1)):
        x1 = data1['Date_Month1'][i]+'-'+str(data1['Date_year'][i])
        mon_yr1.append(x1)
    data1['Month_year1'] = mon_yr1
    ini = list(data1[data1['Month_year'] == ini1].index)[0]
    fin = list(data1[data1['Month_year'] == fin1].index)[-1]
    data1.drop(['Month_year'], axis=1, inplace=True)
    output = data1.loc[ini:fin]
    sum_c = []
    sum_c_p = []
    sum_c_2 = []
    con = pd.DataFrame()
    for k in list(output[axis].unique()):
        x = round(output[output[axis] == k]['Amount'].sum(), 2)
        sum_c.append(x)
        sum_c_p.append(round(x*100/output['Amount'].sum(), 2))
        sum_c_2.append(changeP(x))
    con[axis] = list(output[axis].unique())
    con['Amount'] = sum_c
    con['Amount (Rs.)'] = sum_c_2
    con['Sale_Amount (%)'] = sum_c_p
    con.sort_values('Amount', ascending=False, inplace=True)
    con.reset_index(drop=True, inplace=True)
    if (no_cust).upper() == 'ALL' or int(no_cust) > len(con):
        con = con
    else:
        con = con.loc[0:int(no_cust)-1]
    output2 = pd.DataFrame()
    for j in list(output['Month_year1'].unique()):
        sum_1 = []
        sum_2 = []
        sum_3 = []
        test = output[output['Month_year1'] == j]
        for i in list(test[axis].unique()):
            x = round(test[test[axis] == i]['Amount'].sum(), 2)
            sum_1.append(x)
            sum_2.append(round(x*100/test['Amount'].sum(), 2))
            sum_3.append(changeP(x))
        output1 = pd.DataFrame()
        output1[axis] = list(test[axis].unique())
        output1['Amount'] = sum_1
        output1['Amount (Rs.)'] = sum_3
        output1['Sale_Amount (%)'] = sum_2
        output1['Month'] = [j]*len(sum_1)
        if (no_cust).upper() == 'ALL' or len(sum_1) < int(no_cust):
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output2 = pd.concat([output2, output1], axis=0)
        else:
            output1.sort_values('Amount', ascending=False, inplace=True)
            output1.reset_index(drop=True, inplace=True)
            output1 = output1.loc[0:int(no_cust)-1]
            output2 = pd.concat([output2, output1], axis=0)
    # print(output2, con)
   # output2 graph
   # con table
   # parsing the DataFrame in json format.
    json_records1 = output2.reset_index().to_json(orient='records')
    json_records2 = con.reset_index().to_json(orient='records')

    data1 = []
    data2 = []
    data1 = json.loads(json_records1)
    data2 = json.loads(json_records2)
    context = {'graph': data1, 'table': data2}
    # result1 = output2.to_json(orient="split")
    # result2 = con.to_json(orient="split")
    # return (result1, result2)
    # print(context, "hii")
    return (context)
    # return (output2, con)


def past_VI_XII_monthCall():
    return past_VI_XII_month(df_new, "Customer", 6, 2, df_trade)


def foo(x):
    return x + x


# sys.modules[__name__] = foo
