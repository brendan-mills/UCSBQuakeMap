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

td = timedelta(days=7)
pacific = pytz.timezone('US/Pacific')

endtime = datetime.utcnow()
earlier_today = endtime.replace(hour=0, minute=0, second=0, microsecond=0)

starttime =endtime-td

client = STPClient(verbose=True)
client.connect()   # Open a connection.

# Download a catalog.
cat = client.get_events(times=[starttime, endtime],gtypes='l')

# Disconnect from the STP server.
client.disconnect()

#sets up empty lists to 
times = []
lats = []
lons = []
deps = []
magnitudes = []
magnitudestype = []
for event in cat:
    if len(event.origins) != 0 and len(event.magnitudes) != 0:
        times.append(event.origins[0].time.datetime)
        lats.append(event.origins[0].latitude)
        lons.append(event.origins[0].longitude)
        deps.append(event.origins[0].depth)
        magnitudes.append(event.magnitudes[0].mag)
        magnitudestype.append(event.magnitudes[0].magnitude_type )



df = pd.DataFrame({'lat':lats,'lon':lons,'depth':deps,
                   'mag':magnitudes,'type':magnitudestype},
                  index = times)
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
    meta = df.index,
    text = df['mag'],
    marker = dict(
        size = df['mag']**2,
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
        lonaxis_range= [ -125, -114 ],
        lataxis_range= [ 31, 42 ],
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
