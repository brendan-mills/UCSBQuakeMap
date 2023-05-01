'''
Brendan Mills

'''
import numpy as np
import obspy
import time
from datetime import datetime, timedelta
from pystp import STPClient
import pandas as pd
import pygmt
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from obspy.core.event import Catalog
import pickle

def cat_to_df(cat):
    '''
    This method takes an obspy catalog and returns a pandas dataframe.
    The df has columns: event id, time, lat, lon, depth, magnitude, and magnitude type
    '''
    #sets up empty lists to populate with catalog info
    ids = []
    times = []
    lats = []
    lons = []
    deps = []
    magnitudes = []
    magnitudestype = []
    for event in cat:
        if len(event.origins) != 0 and len(event.magnitudes) != 0:
            ids.append(event.resource_id)
            times.append(event.origins[0].time.datetime)
            lats.append(event.origins[0].latitude)
            lons.append(event.origins[0].longitude)
            deps.append(event.origins[0].depth)
            magnitudes.append(event.magnitudes[0].mag)
            magnitudestype.append(event.magnitudes[0].magnitude_type )
            
    df = pd.DataFrame({'id':ids,'time':times,'lat':lats,'lon':lons,'depth':deps,
                       'mag':magnitudes,'type':magnitudestype})
    return df

#I want the earthquakes from the past week
td = timedelta(days=7)
#pacific = pytz.timezone('US/Pacific')
endtime = datetime.utcnow()
starttime =endtime-td
#earlier_today = endtime.replace(hour=0, minute=0, second=0, microsecond=0)

client = STPClient(verbose=True)
client.connect()   # Open a connection.
client.set_nevntmax(value=9999)
cat = client.get_events(times=[starttime, endtime],gtypes='l')
df = cat_to_df(cat)
print(df)

# Disconnect from the STP server.
client.disconnect()

df.to_pickle('events.pkl')
