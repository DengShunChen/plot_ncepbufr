import read_diag
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# figure
#ichan = 7
list_chan = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]
sat_platform = 'amsua_n15'
date='2017031512'

for ichan in list_chan :

  fig = plt.figure(figsize=(16,8))
  m = Basemap(lon_0=180)
  m.drawcoastlines()
  m.fillcontinents(color='grey',lake_color='aqua',zorder=0)
  m.drawmapboundary(fill_color='aqua')

  obsfile = 'diag_'+sat_platform+'_ges.'+date
  diag_rad = read_diag.diag_rad(obsfile,endian='big')
  print('total number of obs = ',diag_rad.nobs)
  diag_rad.read_obs()

# print o-f stats for one channel
  idxall = diag_rad.channel == ichan
  nobsall = idxall.sum()
  idx = np.logical_and(np.logical_and(diag_rad.channel == ichan, diag_rad.used == 1), diag_rad.oberr < 1.e9)
#  nobs = idx.sum()
  fitsq = ((diag_rad.hx[idx]-diag_rad.obs[idx])**2).mean()
  print('lat lon',diag_rad.lat[idx],diag_rad.lon[idx])

  m.scatter(diag_rad.lon[idx],diag_rad.lat[idx],5,diag_rad.hx[idx]-diag_rad.obs[idx],marker='o',edgecolors='none')
  txt=plt.title('%s    channel %s     %s' % (sat_platform,ichan,date),fontsize=20)
  plt.savefig(sat_platform+'_'+date+'_'+str(ichan)+'.png')

