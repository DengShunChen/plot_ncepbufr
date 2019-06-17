from __future__ import print_function
import ncepbufr
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

# filename
dtg=17091900
filename='gdas.satwnd.tm00.bufr_d.'+str(dtg)

# string 
hdrstr = 'SAID CLAT CLON YEAR MNTH DAYS HOUR MINU SWCM SAZA GCLONG SCCF SWQM' 
obstr = 'HAMD PRLC WDIR WSPD' 
qcstr = 'OGCE GNAP PCCF'

# figure
fig = plt.figure(figsize=(16,8))

#m = Basemap(lon_0=180)
#m.drawcoastlines()
#m.fillcontinents(color='grey',lake_color='aqua',zorder=0)
#m.drawmapboundary(fill_color='aqua')

m = Basemap(lon_0=140.7,lat_0=0,projection='ortho')
m.drawcoastlines()
m.fillcontinents(color='#cc9966',lake_color='#99ffff',zorder=10)
m.drawmapboundary(fill_color='#99ffff')


lons=[]
lats=[]

# read satellite wind file.
bufr = ncepbufr.open(filename)
bufr.print_table()
while bufr.advance() == 0:
    print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
    while bufr.load_subset() == 0:
        hdr = bufr.read_subset(hdrstr).squeeze()
        satid = int(hdr[0])
        if satid == 173 :
          yyyymmddhh ='%04i%02i%02i%02i%02i' % tuple(hdr[3:8])
          windtype = int(hdr[8])
          qm = hdr[12]
          obdata = bufr.read_subset(obstr).squeeze()
          lat = hdr[1]; lon = hdr[2]
          if windtype == 2 : 
            print('satid, wind type, lat, lon, press, qcflg, time, speed, dir =',\
            satid,windtype,lat,lon,obdata[1],qm,yyyymmddhh,obdata[3],obdata[2])
            if lon < 0 :
               lon = lon + 360 
            lats.append(lat)
            lons.append(lon)
    # only loop over first 4 subsets
  # if bufr.msg_counter == 100: break
bufr.close()

print(lons,lats)
x,y = m(lons,lats)

m.scatter(x,y,1,color='r',marker='o',edgecolors='none',zorder=20)
txt=plt.title(' Himawari-8 AMV  %s  : visible'  % (str(dtg)),fontsize=20)

plt.savefig('H-8_SATWND_'+str(dtg)+'.png')

