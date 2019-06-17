from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt



# figure
fig = plt.figure(figsize=(16,8))

m = Basemap(lon_0=120,lat_0=0,projection='ortho')
m.drawcoastlines()
m.fillcontinents(color='grey',lake_color='aqua',zorder=10)
m.drawmapboundary(fill_color='aqua')




plt.show()

