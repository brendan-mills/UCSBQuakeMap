import sys
import numpy as np
import obspy
import time
from datetime import datetime, timedelta
from pystp import STPClient
import pandas as pd
import pygmt
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pytz
import pickle
import folium

def plot_plotly():
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon = df['lon'],
        lat = df['lat'],
        meta = df['time'],
        text = df['mag'],
        marker = dict(
            size = 1.25*df['mag']**2,
            line_width = 0
        ),
        hovertemplate =
        '<i>Date</i>: $%{meta}'+
        '<br><b>Magnitude</b>: %{text}<br>'
        ))
    fig.update_layout(
        showlegend=True,
        title = go.layout.Title(
            text = 'Title Here'),
        geo = go.layout.Geo(
            resolution = 50,
            showframe = True,
            showcoastlines = True,
            landcolor = "rgb(229, 229, 229)",
            coastlinecolor = "grey",
            projection_type = 'mercator',
            lonaxis_range= [ -121, -114 ],
            lataxis_range= [ 31, 37 ],
        ),
    )
    fig.update_geos(
        showsubunits=True, subunitcolor="white"
    )
    fig.show()

def plot_gmt():
    '''
    This method prints the data using pygmt
    '''
    region = [
        df.lon.min() - 1,
        df.lon.max() + 1,
        df.lat.min() - 1,
        df.lat.max() + 1,
    ]
    print(region)
    fig = pygmt.Figure()
    fig.basemap(region=region, projection="M15c", frame=True)
    fig.coast(land="black", water="skyblue")
    fig.plot(
        x=df.lon,
        y=df.lat,
        size= 0.5 * (2**df.mag),
        style="cc",
        fill="white",
        pen="black",
    )
    fig.show()

def get_color(quake_time):
    '''
    This helper method takes a time and determines if it happens within one hour or one day and appropriately returns a color for the event
    '''
    td = datetime.utcnow() - quake_time
    week = timedelta(days=7)
    day = timedelta(days=1)
    hour = timedelta(hours=1)
    #determine how recently it happened
    if td < hour:
        c = 'red'
    elif td < day:
        c = 'orange'
    else:
        c = 'yellow'
    return c
    
def localize_df(df):
    '''
    This method takes a dataframe and looks for a time column,
    it if finds one it returns a copy of the df with a column
    of the assiciated times in the pacific time zone.
    '''
    pacific = pytz.timezone('US/Pacific')
    df_out = df.copy()
    times = df['time']
    loc_times = []
    for t in times:
        utc_time = pytz.utc.localize(t)
        loc_time = utc_time.astimezone(pacific)
        loc_times.append(loc_time)
    df_out['loc_time'] = loc_times
    return df_out

def plot_folium(df):
    m = folium.Map(location=[34, -118],tiles="Stamen Terrain",
        width="%100",
        height="%100",
        zoom_start=6.5)
    tooltip = "Click for info!"
    
    #Iterate over all the rows(quakes) in the dataframe
    for i, row in df.iterrows():
        #this corrects for a magnitude earthquake of 0
        if row['mag'] == 0:
            row['mag'] = 0.001
        time = row['loc_time'].strftime("%H:%M:%S")
        date = row['loc_time'].strftime("%m/%d/%Y")
        c = get_color(row['time'])
        
        #set up the text to display
        iframe = folium.IFrame(date + '<br>Local Time: ' + time + '<br>' + 'Mag: ' + str(row['mag']) + ' ' + row['type'] + '<br>' + 'Depth: ' + str(row['depth']) + f' km<br>SCEDC info <a href="https://scedc.caltech.edu/recent/Quakes/ci{row["id"]}.html" target="_blank">here</a>')
        
        #place the marker
        popup = folium.Popup(iframe, min_width=200, max_width=200)
        folium.CircleMarker(location=(row['lat'],row['lon']),
            radius=1.5*row['mag']**2,
            color=c,
            fill_color=c,
            tooltip=tooltip,
            popup=popup).add_to(m)
    m.save('index.html')
#read dataframe
df = pd.read_pickle('events.pkl')
#add local time column
df = localize_df(df)
colors = ['#808080', '#ffff66', '#ff4d4d']

plot_folium(df)
