#!/usr/bin/env python
from __future__ import print_function
import ncepbufr
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


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

#hdstr1 ='SAID SIID FOVN YEAR MNTH DAYS HOUR MINU SECO CLAT CLON CLATH CLONH HOLS'
hdstr1 ='SAID CLAT CLON'
#hdstr2 ='SAZA SOZA BEARAZ SOLAZI'

# read amsua radiance file.
dtg=17091900
sat_name='atms'
filename='gdas.'+sat_name+'.tm00.bufr_d.'+str(dtg)
print('filename=',filename)

bufr = ncepbufr.open(filename)
bufr.print_table()
while bufr.advance() == 0:
    print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
    while bufr.load_subset() == 0:
        hdr1 = bufr.read_subset(hdstr1).squeeze()
#       hdr2 = bufr.read_subset(hdstr2).squeeze()
        insatid = int(hdr1[0])
        if insatid not in satids:
          satids.append(insatid)
          lons[insatid] = []
          lats[insatid] = []

        rlat = hdr1[1]
        rlon = hdr1[2]
        if rlon < 0:
          rlon = rlon + 360
        lats[insatid].append([rlat])
        lons[insatid].append([rlon])

#        print('lat lon ',hdr1[9],hdr1[10])
#       yyyymmddhhss ='%04i%02i%02i%02i%02i%02i' % tuple(hdr1[3:9])
#       # for satellite id, see common code table c-5
#       # (http://www.emc.ncep.noaa.gov/mmb/data_processing/common_tbl_c1-c5.htm#c-5)
#       # for sensor id, see common code table c-8
#       # (http://www.emc.ncep.noaa.gov/mmb/data_processing/common_tbl_c8-c14.htm#c-8)
#        print('sat id,sensor id, lat, lon, yyyymmddhhmmss =',int(hdr1[0]),\
#       int(hdr1[1]),hdr1[9],hdr1[10],yyyymmddhhss)
#       obs = bufr.read_subset('TMBR',rep=True).squeeze()
#       nchanl = len(obs)
#       for k in range(nchanl):
#           print('channel, tb =',k+1,obs[k])
#   # only loop over first 4 subsets
#    if bufr.msg_counter == 100: break
bufr.close()

mc = ['k', 'r', 'g', 'b', 'm','c','y','hotpink','orange','aqua','purple']

#:print(lats,lons)
for s,satid in enumerate(satids):
  print(satid)
  if len(lons[satid]) == 0:
    continue
    print('length = 0 ,'+satid)
  else:
    print('lats =',len(lats[satid]),'lons =',len(lons[satid]))
  x,y = m(np.asarray(lons[satid]),np.asarray(lats[satid]))
  plt.scatter(x,y,1,color=mc[s],marker='o',edgecolors='none',zorder=20,label=satid)

txt=plt.title('ATMS  %s'  % (str(dtg)),fontsize=20)
plt.legend(ncol=8,loc=8,bbox_to_anchor=(0.5,-0.1),markerscale=2)
plt.savefig('ATMS_'+str(dtg)+'.png')
plt.show()



