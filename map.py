import numpy as np
import pandas as pd
import time, json, requests
from datetime import datetime
import matplotlib
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
data = json.loads(requests.get(url=url).json()['data'])
data2=data['areaTree'][0]['children']

dictionary = {}
for data3 in data2:
   key=data3['name']
   value=data3['total']['confirm'] # query only confirmed
   #value=data3['total']
   dictionary[key]=value


print(dictionary)

"""plot diagnoised patient based on province"""
data = dictionary

lat_min = 0
lat_max = 60
lon_min = 70
lon_max = 140

handles = [
   matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
   matplotlib.patches.Patch(color='#ff7b69', alpha=1, linewidth=0),
   matplotlib.patches.Patch(color='#bf2121', alpha=1, linewidth=0),
   matplotlib.patches.Patch(color='#7f1818', alpha=1, linewidth=0),
   matplotlib.patches.Patch(color='black', alpha=1, linewidth=0),

]
labels = ['1-9 cases', '10-99 cases', '100-999 cases', '1000 cases', '>5000 cases']

fig = matplotlib.figure.Figure()

axes = fig.add_axes((0.1, 0.12, 0.8, 0.8))  # rect = l,b,w,h
fig, axes = plt.subplots()
fig.set_size_inches(10, 12)  # canvas size

m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
m.readshapefile('./china', 'province', drawbounds=True)
m.drawcoastlines(color='green')
m.drawcountries(color='black')
m.drawparallels(np.arange(lat_min, lat_max, 10), labels=[1, 0, 0, 0])  # draw Longitude
m.drawmeridians(np.arange(lon_min, lon_max, 10), labels=[0, 0, 0, 1])  # draw Latitude

for info, shape in zip(m.province_info, m.province):
   pname = info['OWNER'].strip('\x00')
   fcname = info['FCNAME'].strip('\x00')
   if pname != fcname:
      continue

   for key in data.keys():
      if key in pname:
         if data[key] == 0:
            color = '#f0f0f0'
         elif data[key] < 10:
            color = '#ffaa85'
         elif data[key] < 100:
            color = '#ff7b69'
         elif data[key] < 1000:
            color = '#bf2121'
         elif data[key] < 5000:
            color = '#7f1818'
         else:
            color = 'black'
         break

   poly = Polygon(shape, facecolor=color, edgecolor=color)

   axes.add_patch(poly)

axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.11), loc='lower center', ncol=5)

axes.set_title("2019-nCoV realtime map")
FigureCanvasAgg(fig)
fig.savefig('2019-nCoV realtime map')

plt.show()