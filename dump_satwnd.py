#!/usr/bin/env python 
from __future__ import print_function
import ncepbufr

# filename
dtg=18060400
filename='gdas.satwnd.tm00.bufr_d.'+str(dtg)

# string 
hdrstr = 'SAID CLAT CLON YEAR MNTH DAYS HOUR MINU SWCM SAZA GCLONG SCCF SWQM' 
obstr = 'HAMD PRLC WDIR WSPD' 
qcstr = 'OGCE GNAP PCCF'

# read satellite wind file.
bufr = ncepbufr.open(filename)
bufr.print_table()
satids = []
satid = []
while bufr.advance() == 0:
    print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
    while bufr.load_subset() == 0:
        hdr = bufr.read_subset(hdrstr).squeeze()
        satid = int(hdr[0])
    if satid not in satids:
        satids.append(satid)
bufr.close()
print(satids)

