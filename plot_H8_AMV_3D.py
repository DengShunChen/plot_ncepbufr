from __future__ import print_function
import ncepbufr
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections  import PolyCollection
import matplotlib.pyplot as plt
import math

# filename
dtg=17091900
filename='gdas.satwnd.tm00.bufr_d.'+str(dtg)

# string 
hdrstr = 'SAID CLAT CLON YEAR MNTH DAYS HOUR MINU SWCM SAZA GCLONG SCCF SWQM' 
obstr = 'HAMD PRLC WDIR WSPD' 
qcstr = 'OGCE GNAP PCCF'

map = Basemap(lon_0=180)
#m.drawcoastlines()
#m.fillcontinents(color='grey',lake_color='aqua',zorder=0)
#m.drawmapboundary(fill_color='aqua')

#map = Basemap(lon_0=140.7,lat_0=0,projection='ortho')
#map.drawcoastlines()
#map.fillcontinents(color='#cc9966',lake_color='#99ffff',zorder=10)
#map.drawmapboundary(fill_color='#99ffff')

# figure
fig = plt.figure(figsize=(16,8))
ax = Axes3D(fig)

polys = []
for polygon in map.landpolygons:
    polys.append(polygon.get_coords())

lc = PolyCollection(polys, edgecolor='#cc9966',
                    facecolor='#cc9966', closed=False)

ax.add_collection3d(lc)
ax.add_collection3d(map.drawcoastlines(linewidth=0.25))

lons=[]
lats=[]
pres=[]

# read satellite wind file.
bufr = ncepbufr.open(filename)
bufr.print_table()
while bufr.advance() == 0:
    print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
    while bufr.load_subset() == 0:
        hdr = bufr.read_subset(hdrstr).squeeze()
        satid = int(hdr[0])
        if satid != 1733 :
          yyyymmddhh ='%04i%02i%02i%02i%02i' % tuple(hdr[3:8])
          windtype = int(hdr[8])
          qm = hdr[12]
          obdata = bufr.read_subset(obstr).squeeze()
          lat = hdr[1]; lon = hdr[2]
#         print('satid, wind type, lat, lon, press, qcflg, time, speed, dir =',\
#         satid,windtype,lat,lon,obdata[1],qm,yyyymmddhh,obdata[3],obdata[2])
          if lon < 0 :
              lon = lon + 360 
          lats.append(lat)
          lons.append(lon)
          pres.append(obdata[1])
    # only loop over first 4 subsets
    if bufr.msg_counter == 4: break
bufr.close()

#print(lons,lats)
#print(pres)

#x, y = map(lons,lats)
#ax.scatter(x,y,zs=pres,c='r',marker='o')

#ax.scatter(lons,lats,zs=pres,c='r',marker='o')
txt=plt.title(' Himawari-8 AMV  %s'  % (str(dtg)),fontsize=20)

plt.show()

#plt.savefig('H-8_AMV_3D_'+str(dtg)+'.png')

