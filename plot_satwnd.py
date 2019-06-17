#!/usr/bin/env python 
import ncepbufr
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# filename
dtg='17091912'
filename='gdas.satwnd.tm00.bufr_d.'+dtg

# string 
hdrstr = 'SAID CLAT CLON YEAR MNTH DAYS HOUR MINU SWCM SAZA GCLONG SCCF SWQM' 
obstr = 'HAMD PRLC WDIR WSPD' 
qcstr = 'OGCE GNAP PCCF'

# figure
fig = plt.figure(figsize=(16,8))

m = Basemap(lon_0=180)
map_style = 1

if map_style == 1 :
  m.drawmapboundary(fill_color='#A6CAE0',linewidth=0)
  m.fillcontinents(color='grey',alpha=0.7,lake_color='grey',zorder=10)
  m.drawcoastlines(linewidth=0.1,color="white")
else : 
  m.drawcoastlines()
  m.fillcontinents(color='grey',lake_color='aqua',zorder=0)
  m.drawmapboundary(fill_color='aqua')

satids = []

lons = {}
lats = {}

# read satellite wind file.
bufr = ncepbufr.open(filename)
bufr.print_table()
while bufr.advance() == 0:
    print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
    while bufr.load_subset() == 0:
      hdr = bufr.read_subset(hdrstr).squeeze()
      insatid = int(hdr[0])

      # create container
      if insatid not in satids:
        satids.append(insatid)
        lons[insatid] = []
        lats[insatid] = []

#     yyyymmddhh ='%04i%02i%02i%02i%02i' % tuple(hdr[3:8])
#     windtype = int(hdr[8])
#     qm = hdr[12]
#     obdata = bufr.read_subset(obstr).squeeze()
      lat = hdr[1]; lon = hdr[2]
      if lon < 0 :
        lon = lon + 360 
      lats[insatid].append([lat])
      lons[insatid].append([lon])
#   if bufr.msg_counter == 10000: break
bufr.close()
print('satids =',satids)

mc = ['k', 'r', 'g', 'b', 'm','c','y','hotpink','orange','aqua','purple','pink','darkblue']

print(lats,lons)
for s,satid in enumerate(satids):
  print(satid)
  if len(lons[satid]) == 0:
    continue
    print('length = 0 ,'+satid)
  else: 
    print('lats =',len(lats[satid]),'lons =',len(lons[satid]))
  x,y = m(np.asarray(lons[satid]),np.asarray(lats[satid]))
  plt.scatter(x,y,1,color=mc[s],marker='o',edgecolors='none',zorder=20,label=satid)

txt=plt.title('AMV  %s'  % (dtg),fontsize=20)
plt.legend(ncol=8,loc=8,bbox_to_anchor=(0.5,-0.1),markerscale=2)
plt.savefig('SATWND_'+dtg+'.png')
plt.show()

