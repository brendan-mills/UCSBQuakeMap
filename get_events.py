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

def get_cat(cl,t0, t2):
    '''
    Recursively gets earthquakes from the client for a given time
    returns an obspy catalog
    '''
    sub_cat = cl.get_events(times=[t0, t2],gtypes='l')
    if len(sub_cat) >= 90:
        t1 = (t2-t0)/2 + t0
        c1 = get_cat(cl, t0, t1)
        c2 = get_cat(cl, t1, t2)
        return c1 + c2
    else:
        return sub_cat

#I want the earthquakes from the past week
td = timedelta(days=7)
#pacific = pytz.timezone('US/Pacific')
endtime = datetime.utcnow()
starttime =endtime-td
#earlier_today = endtime.replace(hour=0, minute=0, second=0, microsecond=0)

client = STPClient(verbose=True)
client.connect()   # Open a connection.
#sub_cat = client.get_events(times=[starttime, endtime],gtypes='l')
df = cat_to_df(get_cat(client, starttime, endtime))
print(df)

# Disconnect from the STP server.
client.disconnect()

df.to_pickle('events.pkl')
