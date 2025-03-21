import itertools
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import serial
import time
import re
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import pandas as pd



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



fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(20, 8))

line1, = ax1.plot([], [], "ro-", lw=2, label='Outer Temperature(°C)')
line2, = ax2.plot([], [], "ro-", lw=2, label='Outer Humidity(%RH)')
line3, = ax3.plot([], [], "ro-", lw=2, label='Inner Temperature(°C)')
line4, = ax4.plot([], [], "ro-", lw=2, label='Inner Humidity(%RH)')

ax1.set_xlabel('Time')
ax1.set_ylabel('Tempe')
ax1.set_title('Outer Temperature')

ax2.set_xlabel('Time')
ax2.set_ylabel('Hum')
ax2.set_title('Outer Humidity')

ax3.set_xlabel('Time')
ax3.set_ylabel('Tempe')
ax3.set_title('Inner Temperature')

ax4.set_xlabel('Time')
ax4.set_ylabel('Hum')
ax4.set_title('Inner Humidity')

# Add legends to each subplot
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()

ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid()

xdata, y1data,y2data,y3data,y4data,y5data,y6data = [], [], [], [], [], [], []


def data_gen():
    for cnt in itertools.count():
                
        time.sleep(0.1)
        s.write('ReadTemp'.encode())
        time.sleep(0.1)
        bytesToRead = s.inWaiting()
        msg = s.read(bytesToRead).decode()
        OutIn = msg.split("<")

        outTemp,outHum = re.findall( r'\d+\.*\d*', OutIn[0] )
        inTemp,inHum = re.findall( r'\d+\.*\d*', OutIn[1] )

        outTemp, outHum, inTemp, inHum = float(outTemp), float(outHum), float(inTemp), float(inHum)
        
        outDew =  Dew(outTemp,outHum)
        inDew =  Dew(inTemp,inHum)

        y1 = outTemp
        y2 = outHum
        y3 = inTemp
        y4 = inHum
        y5 = outDew
        y6 = inDew
        yield y1, y2, y3, y4, y5, y6

def init():
# Set up the axis limits for all subplots
    for ax in (ax1, ax2, ax3, ax4):
        date_format = mdates.DateFormatter(' %H:%M:%S')
        ax.xaxis.set_major_formatter(date_format)

    for ax in (ax1, ax2):    
        ax.set_ylim(23,28)
    for ax in (ax3, ax4):    
        ax.set_ylim(15,22)

    del xdata[:]
    del y1data[:]
    del y2data[:]
    del y3data[:]
    del y4data[:]

    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    line4.set_data(xdata, y4data)
    return line1, line2, line3, line4,

def updateAx(ax,xdata,ydate,y):

    # Set x-axis limits to show the last 10 points and extend 0.5 seconds beyond the current time

    if len(xdata) > 10:
        # Extending x-axis 0.8 seconds beyond the latest time

        time_extension = xdata[-1] 
        timeExtLeft = xdata[-10] 
        ax.set_xlim(timeExtLeft, time_extension)
    
    # Adjust y-axis to center the current value
    current_y_range = 0.5 * max(abs(min(ydate)), abs(max(ydate)))  # Ensure some margin
    mid_y_value = y
    ax.set_ylim(mid_y_value - current_y_range, mid_y_value + current_y_range)

    ax.relim()
    ax.autoscale_view()
    fig.autofmt_xdate()  # Format the x-axis to show time

    ax.text(0.95, 0.75, f"{y :+05.2f}", transform=ax.transAxes, 
        size=16, ha = "center", color='#777777', family = "Monospace",
        bbox=dict(facecolor='white', alpha=1))
    
def run(data):

        
    current_time = datetime.now().replace(microsecond=0) # return a time without microsecond
    xdata.append(current_time)

    # update the data
    y1, y2, y3, y4, y5, y6 = data

    y1data.append(y1)
    y2data.append(y2)
    y3data.append(y3)
    y4data.append(y4)
    y5data.append(y5)
    y6data.append(y6)

    updateAx(ax1,xdata,y1data,y1)
    updateAx(ax2,xdata,y1data,y2)
    ax2.text(0.8, 1, f"Outer Dew:\n{y5 :.2f}", transform=ax2.transAxes, 
        size=16, ha = "left", color='#777777', family = "Monospace",
        bbox=dict(facecolor='white', alpha=1))
    
    updateAx(ax3,xdata,y1data,y3)
    updateAx(ax4,xdata,y1data,y4)
    ax4.text(0.8, 1, f"Inner Dew:\n{y6 :.2f}", transform=ax4.transAxes, 
        size=16, ha = "left", color='#777777', family = "Monospace",
        bbox=dict(facecolor='white', alpha=1))

    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    line4.set_data(xdata, y4data)

    # Save data to CSV
    data = np.column_stack((xdata, y1data,y2data,y5data,y3data,y4data,y6data))
    df = pd.DataFrame(data, columns=['time','Outer Temperature','Outer Humidity','Outer Dew point',
                                    'Inner Temperature','Inner Humidity','Inner Dew point'])
    df.to_csv('#./code/temper/data/Data.csv', index=False)
    df.to_excel('#./code/temper/data/dataExcel.xlsx', index = False)

    return line1, line2, line3, line4,

ani = animation.FuncAnimation(fig, run, data_gen, interval=1000, init_func=init, save_count=20)
#interval: Delay between frames in milliseconds.
plt.show()


