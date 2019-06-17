from __future__ import print_function
import ncepbufr
from mpl_toolkits.basemap import Basemap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math


dtg=16062100 
filename='gdas1.prepbufr.'+str(dtg)

# prefix
hdstr='SID XOB YOB DHR TYP ELV SAID T29'
obstr='POB QOB TOB ZOB UOB VOB PWO MXGS HOVI CAT PRSS TDO PMO'
qcstr='PQM QQM TQM ZQM WQM NUL PWQ PMQ'
oestr='POE QOE TOE NUL WOE NUL PWE'

#msg_list=['SATWND','SFCSHP','ASCATW','RASSDA','ADPSFC','ADPUPA','AIRCFT','VADWND','PROFLR']
msg_list=['SATWND']

for plot_msg in msg_list : 

  # figure
  fig = plt.figure(figsize=(16,8))
  m = Basemap(lon_0=180)
  m.drawcoastlines()
  m.fillcontinents(color='grey',lake_color='aqua',zorder=0)
  m.drawmapboundary(fill_color='aqua')

  lon = [ ]
  lat = [ ]
  obs_satwnd = [ ]


  # read prepbufr file.
  bufr = ncepbufr.open(filename)
  bufr.print_table() # print embedded table
  #bufr.dump_table('prepbufr.table') # dump table to file
  bufr.dump_table('prepobs_prep.bufrtable') # dump table to file
  while bufr.advance() == 0: # loop over messages.
      print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
      #bufr.read_subset(obstr) # should raise subset not loaded error
      while bufr.load_subset() == 0: # loop over subsets in message.
          if bufr.msg_type  == plot_msg :
            hdr = bufr.read_subset(hdstr).squeeze()
            lon.append([hdr[1]])
            lat.append([hdr[2]])
            if plot_msg  == 'SATWND' :
              obs = bufr.read_subset('UOB VOB')
              wind = math.sqrt(obs[0]*obs[0]+obs[1]*obs[1])
              obs_satwnd.append([wind])
     #     print(hdr[1],hdr[2],wind)        
     #  station_id = hdr[0].tostring()
     #  obs = bufr.read_subset(obstr)
     #  nlevs = obs.shape[-1]
     #  oer = bufr.read_subset(oestr)
     #  qcf = bufr.read_subset(qcstr)
      # print('station_id, lon, lat, time, station_type, levels =',\
      # station_id,hdr[1],hdr[2],hdr[3],int(hdr[4]),nlevs)
      # m.scatter(hdr[1],hdr[2],c='r',marker='o',)
       #for k in range(nlevs):
       #    if nlevs > 1:
       #        print('level',k+1)
       #    print('obs',obs[:,k])
       #    print('oer',oer[:,k])
       #    print('qcf',qcf[:,k])
    # stop after first 2 messages.
   #if bufr.msg_counter == 1000: break
  bufr.close()

  if plot_msg == 'SATWND' :
    plt.scatter(lon,lat,1,obs_satwnd,cmap=plt.cm.hot_r,marker='o',edgecolors='none',zorder=10)
    plt.colorbar()
    txt=plt.title('Wind Speed of SATWND %s'  % (bufr.msg_date),fontsize=20)
  else :
    plt.scatter(lon,lat,15,'r',marker='o',edgecolors='none',zorder=10)
    txt=plt.title('%s %s'  % (plot_msg,bufr.msg_date),fontsize=20)

  plt.show()
  plt.savefig(plot_msg+'.pdf')


