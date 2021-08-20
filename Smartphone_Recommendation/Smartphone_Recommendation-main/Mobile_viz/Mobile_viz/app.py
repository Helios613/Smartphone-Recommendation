from flask import Flask, render_template, request, redirect
import os
from flask.helpers import url_for
app=Flask(__name__)


import plotly.graph_objects as go
import plotly.offline as pyo
import time
import csv,sqlite3
import numpy as np
import pandas as pd
from plotly.tools import make_subplots
from plotly.subplots import make_subplots
import plotly.express as px
import shutil

@app.route('/')
def redirect_pref():
    return redirect(url_for('plots'))

@app.route('/update')
def index():
    path=os.getcwd()
    path_extracter=path+"/spiders/mobile_data.py"
    os.system("python "+path_extracter)
    return redirect(url_for('plots'))

@app.route('/plots', methods=["POST","GET"])
def plots():
    path=os.getcwd()
    path=path.replace("\\","/")
    path=path.rsplit('/',1)[0]
    
    path_plots=path+"/Mobile_viz/templates"
    

    pathdb=path+"/Mobiles.db"
    #pathdb="C:/Users/DELL/Desktop/Data_Vis/Jcomponent/Mobile_viz/Mobiles.db"
    
    conn= sqlite3.connect(pathdb)
    curr= conn.cursor()
    
    price_cap=request.args.get('prices')#input("Enter the Price Cap: ")
    if(type(price_cap).__name__=='NoneType' or price_cap==''):
        curr.execute("select max(price) from smartphones where price !=''")
        price_cap=curr.fetchone()[0]
    select_price="""select * from SmartPhones 
    where 
    Price <= '"""+str(price_cap) +"""' and 
    Price != ''  and 
    Geekbench5_Multi_Core_Score != '' and 
    Geekbench5_Single_Core_Score != '' and 
    strftime('%Y%m%d',Update_Date) > strftime('%Y%m%d',DATE('now','-2 month'))
    ORDER BY Overall_Score desc"""
    
    choice='y'

    if (choice=='y'):
        # preferences=input("""Enter the list of features important to you...\n
        # 1: Battery\n
        # 2: Camera\n
        # 3: General Connectivity\n
        # 4: Display\n
        # 5: Performance\n
        # 6: Software\n
        # 7: Sound\n""")
        dicto={
            1: 'Battery_Score',
            2: 'Camera_Score',
            3: 'Connectivity_Score',
            4: 'Display_Score',
            5: 'Performance_Score',
            6: 'Software_Score',
            7: 'Sound_Score'
        }
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
        pref_arr=request.args.getlist('mymultiselect')#preferences.rsplit(' ')
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
    rowsl=curr.fetchall()
    rows=rowsl
    if(len(rows)>3):    
        rows=rows[0:3]

    # 0 - Antutu
    # 1 - Battery       85
    # 2 - Camera        85
    # 3 - Connectivity  75
    # 4 - Display       70
    # 5 - Geekbench5_Multicore
    # 6 - Geekbench5_Singlecore
    # 7 - Overall
    # 8 - Performance   80
    # 9 - Phone_Name
    # 10 - Price
    # 11 - Software     80
    # 12 - Sound        75
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
            title=go.layout.Title(text='SmartPhone Comparison... Price Upper Limit(USD): '+str(price_cap)),
            polar={'radialaxis': {'visible': True}},
            showlegend=True
        )
    )

    if (os.path.isfile(path_plots+"/radar.html")):
        os.remove(path_plots+"/radar.html")
    fig.write_html(path_plots+"/radar.html")

    #pyo.plot(fig)

    #2

    Phone_Name=[]
    Overall_Score=[]
    price=[]
    performance=[]
    camera=[]
    software=[]
    battery=[]
    connectivity=[]
    display=[]
    sound=[]
    for i in range(len(rows)):
        Phone_Name.append(rows[i][9])
        Overall_Score.append(rows[i][7])
        price.append(rows[i][10])
        performance.append(rows[i][8])
        camera.append(rows[i][2])
        software.append(rows[i][11])
        battery.append(rows[i][1])
        connectivity.append(rows[i][3])
        display.append(rows[i][4])
        sound.append(rows[i][12])
    fig1= go.Figure()
    fig1.add_trace(go.Bar(x=Phone_Name, y=Overall_Score,text=Overall_Score,textposition="auto",hovertemplate="<b>%{x}</b><br><br>" +"Overall Score: %{y}<br><extra></extra>"))
    fig1.update_layout(go.Layout(title='Overall score comparison (Bar Chart)', xaxis_title='Phone Name', yaxis_title='Overall Score'))
    if (os.path.isfile(path_plots+"/bar.html")):
        os.remove(path_plots+"/bar.html")
    fig1.write_html(path_plots+"/bar.html")

    #pyo.plot(fig1)

    #3

    fig2= go.Figure()
    fig2.add_trace(go.Scatter(x=Phone_Name, y=price, mode='lines+markers',hovertemplate="<b>%{x}</b><br><br>" +"Price: %{y}<br><extra></extra>"))
    fig2.update_layout(go.Layout(title='Price comparison (Line Chart)',xaxis_title='Phone Name', yaxis_title='Price'))
    fig2.update_layout(yaxis_range=[0,int(price_cap)+100])
    if (os.path.isfile(path_plots+"/scatter.html")):
        os.remove(path_plots+"/scatter.html")
    fig2.write_html(path_plots+"/scatter.html")
    #pyo.plot(fig2)

    #4
    phone_name=[]
    price=[]
    performance=[]
    camera=[]
    software=[]
    battery=[]
    connectivity=[]
    display=[]
    sound=[]
    for i in range(len(rowsl)):
        phone_name.append(rowsl[i][9])
        price.append(rowsl[i][10])
        performance.append(rowsl[i][8])
        camera.append(rowsl[i][2])
        software.append(rowsl[i][11])
        battery.append(rowsl[i][1])
        connectivity.append(rowsl[i][3])
        display.append(rowsl[i][4])
        sound.append(rowsl[i][12])

    fig4 = go.Figure(data=
    go.Parcoords(
        line = dict(color = price, colorscale = 'ylorrd', showscale = True, cmin = -1000, cmax = 3000),
        dimensions = list([
            dict(range = [0,3000],
                label = "Price", values = price),
            dict(range = [0,500],
                label = 'Performance', values = performance),
            dict(range = [0,500],
                label = 'Camera', values = camera),
            dict(range = [0,500],
                label = 'Software', values = software),
            dict(range = [0,500],
                visible = False,
                label = 'Battery', values = battery),
            dict(range = [0,500],
                label = 'Connectivity', values = connectivity),
            dict(range = [0,500],
                label = 'Display', values = display),
            dict(range = [0,500],
                label = 'Sound', values = sound)]),
        )
    )
    if (os.path.isfile(path_plots+"/parcoord.html")):
        os.remove(path_plots+"/parcoord.html")
    fig4.write_html(path_plots+"/parcoord.html")


    return render_template('plot.html', rows=rows)

@app.route('/visualization')
def visualization():
    return render_template('visualization.html')

@app.route('/radar')
def radars():
    return render_template('radar.html')

@app.route('/scatter')
def scatter():
    return render_template('scatter.html')
@app.route('/bar')
def bar():
    return render_template('bar.html')

@app.route('/database')
def database():
    path=os.getcwd()
    path=path.replace("\\","/")
    path=path.rsplit('/',1)[0]
    pathdb=path+"/Mobiles.db"
    #pathdb="C:/Users/DELL/Desktop/Data_Vis/Jcomponent/Mobile_viz/Mobiles.db"
    
    conn= sqlite3.connect(pathdb)
    curr= conn.cursor()
    curr.execute("SELECT * FROM smartphones")
    data = curr.fetchall()
    return render_template('database.html', data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/parcoord')
def parcoord():
    return render_template('parcoord.html')

if __name__ == "__main__":
        app.run(debug=True,port=8000)