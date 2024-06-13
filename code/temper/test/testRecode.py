import serial
import re
import DewPoint as DP
import numpy as np
import pandas as pd
import time
from datetime import datetime

timeData, outTempData,outHumData,outDewData,inTempData,inHumData,inDewData = [], [], [], [], [], [], []

s = serial.Serial("COM3")

s.write('Version'.encode())
time.sleep(0.1)
bytesToRead = s.inWaiting()
msg = s.read(bytesToRead).decode()
print(msg)
time.sleep(0.1)

if msg == "TEMPerX232_V2.5\r\n":
    for i in range(10):
        s.write('ReadTemp'.encode())
        time.sleep(0.1)
        bytesToRead = s.inWaiting()
        msg = s.read(bytesToRead).decode()
        OutIn = msg.split("<")

        outTemp,outHum = re.findall( r'\d+\.*\d*', OutIn[0] )
        inTemp,inHum = re.findall( r'\d+\.*\d*', OutIn[1] )

        outTemp, outHum, inTemp, inHum = float(outTemp), float(outHum), float(inTemp), float(inHum)
        
        outDew =  DP.Dew(outTemp,outHum)
        inDew =  DP.Dew(inTemp,inHum)
        currentTime = datetime.now().replace(microsecond=0)

        timeData.append(currentTime)

        # update the data
        outTempData.append(outTemp)
        outHumData.append(outHum)
        outDewData.append(outDew)
        inTempData.append(inTemp)
        inHumData.append(inHum)
        inDewData.append(inDew)
        
        # Save data to CSV
        data = np.column_stack((timeData,outTempData,outHumData,outDewData,
                                inTempData,inHumData,inDewData))
        df = pd.DataFrame(data,columns=['time','Outer Temperature','Outer Humidity','Outer Dew point',
                                         'Inner Temperature','Inner Humidity','Inner Dew point'])
        df.to_csv('Data.csv', index=False)
        df.to_excel('dataExcel.xlsx', index = False)
        time.sleep(1)
