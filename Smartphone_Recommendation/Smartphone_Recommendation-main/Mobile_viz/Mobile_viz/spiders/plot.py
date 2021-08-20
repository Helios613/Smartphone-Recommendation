import plotly.graph_objects as go
import plotly.offline as pyo
import time
import csv,sqlite3
import os
import numpy as np
import pandas as pd
from plotly.tools import make_subplots
from plotly.subplots import make_subplots
import plotly.express as px
import shutil

path=os.getcwd()
path=path.replace("\\","/")
path=path.rsplit('/',1)[0]
pathdb=path+"/Mobiles.db"
conn= sqlite3.connect(pathdb)
curr= conn.cursor()
price_cap=input("Enter the Price Cap: ")
select_price="""select * from smartphones 
where 
price <="""+str(price_cap) +""" and 
price != ''  and 
geekbench5_multi_core_score != '' and 
geekbench5_single_core_score != '' and 
strftime('%Y%m%d',update_date) > strftime('%Y%m%d',DATE('now','-2 month'))
ORDER BY overall_score desc"""
choice=input("Do you have any specific preferences of features you want in the smartphone? (y/n) :") 
choice=input()
if (choice=='y'):
    preferences=input("""Enter the list of features important to you...\n
    1: Battery\n
    2: Camera\n
    3: General Connectivity\n
    4: Display\n
    5: Performance\n
    6: Software\n
    7: Sound\n""")
    dicto={
        1: 'Battery_score',
        2: 'Camera_score',
        3: 'Connectivity_score',
        4: 'Display_score',
        5: 'Performance_score',
        6: 'Software_score',
        7: 'Sound_score'
    }
    #pref_arr=preferences.rsplit(' ')
    dictw={
        1: 0.85,
        2: 0.85,
        3: 0.75,
        4: 0.70,
        5: 0.80,
        6: 0.80,
        7: 0.75
    }
    normalizing_factor=0
    pref_arr=preferences.rsplit(' ')
    for i in range(1,8):
        if str(i) in pref_arr:
            dictw[i]=2*dictw[i]
        normalizing_factor=normalizing_factor+dictw[i]
    print(pref_arr)
    seg_str=''
    for i in range(1,8):
        if (i==1):
            seg_str= dicto[i]+"*"+str(dictw[i])
        else:
            seg_str= seg_str+'+'+ dicto[i]+"*"+str(dictw[i])
    seg_str="("+seg_str+")"+"/"+str(normalizing_factor)
    if seg_str=='':
        select_price="""select * from smartphones 
        where 
        price <='"""+str(price_cap) +"""' and 
        price != '' and
        strftime('%Y%m%d',Update_Date) > strftime('%Y%m%d',DATE('now','-2 month')) 
        ORDER BY overall_score desc"""
    else:
        select_price="""select * from smartphones 
            where 
            price <='"""+str(price_cap) +"""' and 
            price != '' and
            strftime('%Y%m%d',Update_Date) > strftime('%Y%m%d',DATE('now','-2 month')) 
            ORDER BY """+seg_str+" desc"

curr.execute(select_price)
rows=curr.fetchall()
if(len(rows)>3):    
    rows=rows[0:3]

# 0 - Antutu
# 1 - Battery
# 2 - Camera
# 3 - Connectivity
# 4 - Display 
# 5 - Geekbench5_Multicore
# 6 - Geekbench5_Singlecore
# 7 - Overall
# 8 - Performance
# 9 - Phone_Name
# 10 - Price
# 11 - Software
# 12 - Sound
# 13 - Update_Date

print(rows)

categories = ['Battery', 'Camera', 'Connectivity', 'Display', 'Performance', 'Software', 'Sound']
categories = [*categories, categories[0]]
Phone_arr=[]
data_radar=[]
for i in range(len(rows)):
    Phone_arr.append([rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][8], rows[i][11], rows[i][12]])
    Phone_arr[i] = [*Phone_arr[i], Phone_arr[i][0]]
    data_radar.append(go.Scatterpolar(r=Phone_arr[i], theta=categories, name=rows[i][9],hovertemplate="<b>Score: " +"%{r}<br><extra>"+rows[i][9]+"</extra>"))

fig = go.Figure(
    data=data_radar,
    layout=go.Layout(
        title=go.layout.Title(text='SmartPhone Comparison'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True
    )
)




pyo.plot(fig)

#2

Phone_Name=[]
Overall_Score=[]
for i in range(len(rows)):
    Phone_Name.append(rows[i][9])
    Overall_Score.append(rows[i][7])

fig1= go.Figure()
fig1.add_trace(go.Bar(x=Phone_Name, y=Overall_Score,hovertemplate="<b>%{x}</b><br><br>" +"Overall Score: %{y}<br><extra></extra>"))
fig1.update_layout(go.Layout(title='Overall score comparison (Bar Chart)', xaxis_title='Phone Name', yaxis_title='Overall Score'))



pyo.plot(fig1)

#3

fig2= go.Figure()
fig2.add_trace(go.Scatter(x=Phone_Name, y=Overall_Score, mode='lines+markers',hovertemplate="<b>%{x}</b><br><br>" +"Overall Score: %{y}<br><extra></extra>"))
fig2.update_layout(go.Layout(title='Overall score comparison (Line Chart)',xaxis_title='Phone Name', yaxis_title='Overall Score'))


pyo.plot(fig2)
