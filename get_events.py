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
import pytz
from obspy.core.event import Catalog
import pickle

td = timedelta(days=14)
pacific = pytz.timezone('US/Pacific')

endtime = datetime.utcnow()
earlier_today = endtime.replace(hour=0, minute=0, second=0, microsecond=0)

starttime =endtime-td

client = STPClient(verbose=True)
client.connect()   # Open a connection.

def cat_to_df(cat):
    #sets up empty lists to populate with catalog info
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
            
    df = pd.DataFrame({'time':times,'lat':lats,'lon':lons,'depth':deps,
                       'mag':magnitudes,'type':magnitudestype})
    return df

def get_cat(t0, t2):
    sub_cat = client.get_events(times=[t0, t2],gtypes='l')
    if len(sub_cat) >= 50:
        t1 = (t2-t0)/2 + t0
        c1 = get_cat(t0,t1)
        c2 = get_cat(t1,t2)
        return c1 + c2
    else:
        return sub_cat

sub_cat = client.get_events(times=[starttime, endtime],types='eq')
#df = cat_to_df(get_cat(starttime, endtime))
#print(df)

# Disconnect from the STP server.
client.disconnect()



#df.to_pickle('events.pkl')
