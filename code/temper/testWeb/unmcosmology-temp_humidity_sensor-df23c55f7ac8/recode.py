import serial
import re
import numpy as np
import time
import os
#import Library 

import DewPoint as DP
import linuxSer as ls
#import my file

# this will read the data from PCsensor and use DewPoint.py to have the Dew point and save to a txt file

s = serial.Serial(ls.serialPorts())


#for i in range(3):
while True: #for run forever
    s.write('ReadTemp'.encode())
    time.sleep(0.1)
    bytesToRead = s.inWaiting()
    msg = s.read(bytesToRead).decode()
    OutIn = msg.split("<")

    outTemp,outHum = re.findall( r'\d+\.*\d*', OutIn[0] )
    inTemp,inHum = re.findall( r'\d+\.*\d*', OutIn[1] )

    outTempF, outHumF, inTempF, inHumF = float(outTemp), float(outHum), float(inTemp), float(inHum)
    
    outDew =  DP.Dew(outTempF,outHumF)
    inDew =  DP.Dew(inTempF,inHumF)

    lTime = time.localtime()
    fTime = time.strftime( "%Y-%m-%d", lTime )
    
    hTime = time.strftime( "%H:%M:%S", lTime )

    path = 'data'
    fName = '{path}/{date}TEMP.txt'.format( path =path, date = fTime )

    if not os.path.exists(path):
        os.makedirs(path)

    if os.path.isfile(fName):
        file = open(fName, 'a')
    else:
        file = open(fName, 'w')
          
   
    file.write(hTime+", "+outTemp+", "+outDew+", "+outHum+",   "+inTemp+", "+inDew+", "+inHum+" \n")
    time.sleep(30)
    #delay to next run

