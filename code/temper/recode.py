import serial
import re
import numpy as np
import pandas as pd
import time
from datetime import datetime
from pathlib import Path
#import Library 

import DewPoint as DP
import ListingPorts as LP
#import my file

#timeData, outTempData,outHumData,outDewData,inTempData,inHumData,inDewData = [], [], [], [], [], [], []

s = serial.Serial(LP.serial_ports())


for i in range(2):
#while true: #for run forever
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
    currentTime = datetime.now()

    # # update the data
    # timeData.append(currentTime)
    # outTempData.append(outTemp)
    # outHumData.append(outHum)
    # outDewData.append(outDew)
    # inTempData.append(inTemp)
    # inHumData.append(inHum)
    # inDewData.append(inDew)
    
    # Save data to CSV
    data = np.column_stack((currentTime,outTemp,outHum,outDew,
                            inTemp,inHum,inDew))
    df = pd.DataFrame(data,columns=['YYYY-MM-DD HH:MM:SS.micsec',
                                    'Outer Temperature','Outer Humidity','Outer Dew point',
                                    'Inner Temperature','Inner Humidity','Inner Dew point'])


    file_path = f"{currentTime.date()}.csv"
    my_file = Path(file_path)

    if my_file.exists(): # file exists
        df.to_csv(f'{currentTime.date()}.csv', mode = 'a', index=False, header=False)
    else: 
        df.to_csv(f'{currentTime.date()}.csv', index=False)

    time.sleep(0.9)
