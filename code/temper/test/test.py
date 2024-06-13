import serial
import time
from matplotlib.animation import FuncAnimation
import re
import numpy as np

def Dew(T,RH): 
    """
    A well-known empirical approximation used to calculate the dew point
    by Wikipedia https://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point
    """

    # b and c constant for temperature range -40°C to +50°C
    b = 17.625 
    c = 243.04 #°C 
    lam = np.log(RH/100) + (b*T)/(c+T)
    dewPoint = (c*lam)/(b-lam)

    return dewPoint

s = serial.Serial("COM3")

#while True:
for i in range(2):

            
    time.sleep(0.1)
    send = s.write('ReadTemp'.encode())
    time.sleep(0.1)
    bytesToRead = s.inWaiting()
    msg = s.read(bytesToRead).decode()
    OutIn = msg.split("<")

    outTemp,outHum = re.findall( r'\d+\.*\d*', OutIn[0] )
    inTemp,inHum = re.findall( r'\d+\.*\d*', OutIn[1] )

    outTemp, outHum, inTemp, inHum = float(outTemp), float(outHum), float(inTemp), float(inHum)
    
    print(msg)
    print(outTemp,"C, ",outHum,"%RH")
    print(inTemp,"C, ",inHum,"%RH")

    outDew =  Dew(outTemp,outHum)
    inDew =  Dew(inTemp,inHum)

    print(f"{outDew:.2f}C ")
    print(f"{inDew:.2f}C ")
    time.sleep(0.7)
    print("")

