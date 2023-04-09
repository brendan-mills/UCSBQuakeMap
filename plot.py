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

df = pd.read_pickle('events.pkl')
print(df)
region = [
    df.lon.min() - 1,
    df.lon.max() + 1,
    df.lat.min() - 1,
    df.lat.max() + 1,
]
print(region)
fig = go.Figure()
fig.add_trace(go.Scattergeo(
    lon = df['lon'],
    lat = df['lat'],
    meta = df['time'],
    text = df['mag'],
    marker = dict(
        size = 1.25*df['mag']**2,
#        color = colors[i-6],
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

#fig = pygmt.Figure()
#fig.basemap(region=region, projection="M15c", frame=True)
#fig.coast(land="black", water="skyblue")
#fig.plot(
#    x=df.lon,
#    y=df.lat,
#    size= 0.5 * (2**df.mag),
#    style="cc",
#    fill="white",
#    pen="black",
#)
#fig.show()
#plt.scatter(x=df.lon, y=df.lat)
#plt.show()

