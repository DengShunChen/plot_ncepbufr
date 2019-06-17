#!/usr/bin/env python 
from __future__ import print_function
import ncepbufr
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


# filename
dtg=18060400
filename='gdas.gpsro.tm00.bufr_d.'+str(dtg)

dtg = open('/nwp/ncsagfs/GFS/MNH/etc/crdate','r').read().rstrip()
filename='/nwp/ncsagfs/GFS/MNH/workdir/gpsrobufr'

print(filename)
hdrstr ='YEAR MNTH DAYS HOUR MINU PCCF ELRC SAID PTID GEODU'

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

# read gpsro file.
bufr = ncepbufr.open(filename)
bufr.print_table()
while bufr.advance() == 0:
    print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
    while bufr.load_subset() == 0:
        hdr = bufr.read_subset(hdrstr).squeeze()

        insatid = int(hdr[7])
        if insatid not in satids:
          satids.append(insatid)
          lons[insatid] = []
          lats[insatid] = []

   #    yyyymmddhh ='%04i%02i%02i%02i%02i' % tuple(hdr[0:5])
        nreps_this_ROSEQ2 = bufr.read_subset('{ROSEQ2}').squeeze()
        nreps_this_ROSEQ1 = len(nreps_this_ROSEQ2)
        data1b = bufr.read_subset('ROSEQ1',seq=True) # bending angle
   #    data2a = bufr.read_subset('ROSEQ3',seq=True) # refractivity
   #    levs_bend = data1b.shape[1]
   #    levs_ref = data2a.shape[1]
   #    if levs_ref != levs_bend:
   #        print('skip report due to bending angle/refractivity mismatch')
   #        continue
   #    print('sat id,platform transitter id, levels, yyyymmddhhmm =',\
   #    satid,ptid,levs_ref,yyyymmddhh)
   #    print('k, height, lat, lon, ref, bend:')

        for k in range(nreps_this_ROSEQ1):
            rlat = data1b[0,k]
            rlon = data1b[1,k]
            if rlon < 0:
              rlon = rlon + 360
            lats[insatid].append([rlat])
            lons[insatid].append([rlon])

        #   height = data2a[0,k]
        #   ref = data2a[1,k]
        #   for i in range(int(nreps_this_ROSEQ2[k])):
        #       m = 6*(i+1)-3
        #       freq = data1b[m,k]
        #       bend = data1b[m+2,k]
                # look for zero frequency bending angle ob
        #       if int(freq) == 0: break
        #   print(k,rlat,rlon,height,ref,bend)
    # only loop over first 6 subsets
   # if bufr.msg_counter == 6: break
bufr.close()

mc = ['k', 'r', 'g', 'b', 'm','c','y','hotpink','orange','aqua','purple'] 

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

txt=plt.title('GPS RO  %s'  % (str(dtg)),fontsize=20)
plt.legend(ncol=8,loc=8,bbox_to_anchor=(0.5,-0.1),markerscale=2)
plt.savefig('GPSRO_'+str(dtg)+'.png')
plt.show()



