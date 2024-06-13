import itertools
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import serial
import time
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



fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(20, 8))

line1, = ax1.plot([], [], lw=2, label='1')
line2, = ax2.plot([], [], lw=2, label='2')
line3, = ax3.plot([], [], lw=2, label='3')
line4, = ax4.plot([], [], lw=2, label='4')

# Add legends to each subplot
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()

ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid()

xdata, y1data,y2data,y3data,y4data = [], [], [], [], []


def data_gen():
    for cnt in itertools.count():
        t = cnt
        CurTime = time.strftime("%a, %d %b %Y %X +0000",  time.localtime()) 
        
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
        yield t, y1, y2, y3, y4, y5, y6

def init():
# Set up the axis limits for all subplots
    for ax in (ax1, ax2, ax3, ax4):
        ax.set_xlim(0, 5)
        ax.set_ylim(15,25)



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

def updateAx(ax,t,y):
    
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    xRan = xmax-xmin
    yRan = ymax-ymin

    if t >= xmax:
        ax.set_xlim(xmax-1, xmax + xRan)
        ax.figure.canvas.draw()
    if y >= ymax:
        ax.set_ylim(ymax-1, ymax + yRan)
        ax.figure.canvas.draw()

    # if t <= xmin:
    #     ax.set_xlim(xmin - xRan, xmin+1)
    #     ax.figure.canvas.draw()
    if y <= ymin:
        ax.set_ylim(ymin - yRan, ymin+1)
        ax.figure.canvas.draw()

    ax.text(0.95, 0.75, f"{y :+05.2f}", transform=ax.transAxes, 
        size=16, ha = "center", color='#777777', family = "Monospace",
        bbox=dict(facecolor='white', alpha=1))
#
    
def run(data):
    
    # update the data
    t, y1, y2, y3, y4, y5, y6 = data


    xdata.append(t)
    y1data.append(y1)
    y2data.append(y2)
    y3data.append(y3)
    y4data.append(y4)

    updateAx(ax1,t,y1)
    updateAx(ax2,t,y2)
    ax2.text(1.1, 1, f"Outer Dew Point:\n{y5 :.2f}", transform=ax2.transAxes, 
        size=16, ha = "right", color='#777777', family = "Monospace",
        bbox=dict(facecolor='white', alpha=1))
    
    updateAx(ax3,t,y3)
    updateAx(ax4,t,y4)
    ax4.text(1.1, 0.1, f"Inner Dew Point:\n{y6 :.2f}", transform=ax4.transAxes, 
        size=16, ha = "right", color='#777777', family = "Monospace",
        bbox=dict(facecolor='white', alpha=1))

    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)
    line3.set_data(xdata, y3data)
    line4.set_data(xdata, y4data)

    return line1, line2, line3, line4,

# Only save last 100 frames, but run forever
ani = animation.FuncAnimation(fig, run, data_gen, interval=1000, init_func=init,
                              save_count=100)

plt.show()

