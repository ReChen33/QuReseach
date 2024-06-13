#!/usr/bin/python

import sys, os
import time
from simInterface import simInterface
import numpy as np

DIODE_PORT = 8 #port on the SRS box
queryPeriod = 2 #time in seconds between polls to the sim
symLink = 'currentTemperatureLog.txt' #locate of symlink that points to the current log file

def chebysev(i,x):
	return np.cos(i * np.arccos(x))
	
def x(Z, ZL, ZU):
	return ((Z-ZL) - (ZU-Z)) / (ZU - ZL) #see note from Lakeshore about curve10 definition 	

def getCoefftsLS10(voltage):
	#gets chebysev coeffts for lakeshore curve 10
	a = list(np.tile(float('nan'),(1,10))[0])
	
	ZL = 1.32412
	ZU = 1.69812
	if voltage >= ZL and voltage <= ZU:
		a[0] = 7.556358
		a[1] = -5.917261
		a[2] = 0.237238
		a[3] = -0.334636
		a[4] = -0.058642
		a[5] = -0.019929
		a[6] = -0.020715
		a[7] = -0.014814
		a[8] = -0.008789
		a[9] = -0.008554
		return a, [ZL,ZU]
	
	ZL = 1.11732
	ZU = 1.42013	
	
	a.append(float('nan'))
	
	if voltage >= ZL and voltage <= ZU:
		a[0] = 17.304227
		a[1] = -7.894688
		a[2] = 0.453442
		a[3] = 0.002243
		a[4] = 0.158036
		a[5] = -0.193093
		a[6] = 0.155717
		a[7] = -0.085185
		a[8] = 0.078550
		a[9] = -0.018312
		a[10] = 0.039255
		return a, [ZL,ZU]
	
	ZL = 0.923174
	ZU = 1.13935
	
	a.append(float('nan'))
	
	if voltage >= ZL and voltage <= ZU:
		a[0] = 71.818025
		a[1] = -53.799888
		a[2] = 1.669931
		a[3] = 2.314228
		a[4] = 1.566635
		a[5] = 0.723026
		a[6] = -0.149503
		a[7] = 0.046876 
		a[8] = -0.388555
		a[9] = 0.056889
		a[10] = -0.116823
		a[11] = 0.058580
		
		return a, [ZL,ZU]
	
	a.pop()
	
	ZL = 0.079767
	ZU = 0.999614
	if voltage >= ZL and voltage <= ZU:
		a[0] = 287.756797
		a[1] = -194.144823
		a[2] = -3.837903
		a[3] = -1.318325
		a[4] = -0.109120
		a[5] = -0.393265
		a[6] = 0.146911
		a[7] = -0.111192
		a[8] = 0.028877
		a[9] = -0.029286
		a[10] = 0.015619
		return a, [ZL,ZU]
	
	return a, [0,0]

def convertToTemp(voltage, curveFun= getCoefftsLS10):
	
	coeffts, ZLU = curveFun(voltage)
	
	if ZLU == [0,0]: 
		return float('nan')
		
	temp = 0
	
	for coefft in enumerate(coeffts):
		temp = temp + coefft[1] * chebysev(coefft[0], x(voltage, ZLU[0], ZLU[1]))
	
	return temp

	
if __name__ == '__main__':
	
	try:
		fName = sys.argv[1]
	except IndexError:
		fName = None
	
	
		
	if fName != None:
		
		try:
			tf = open(fName,'r')
		except IOError:
			#if the file doesn't exist, then create it
			tf = open(fName,'w')
		finally:
			tf.close()
		
		if os.path.islink(symLink):
			os.remove(symLink)
		#create the symlink
		os.symlink(fName, symLink)
	
	mySim = simInterface()
	mySim.connectToSimPort(DIODE_PORT)
	
	try:
		if mySim.getDeviceID() == 'SIM922': #SIM922 is the diode temperature monitor
			#file.write(time.strftime('Logging begins at: %A %B %d, %Y at %H:%M:%S\n'))
			while True:
				voltages = mySim.getVoltages()
				temps = map(convertToTemp, voltages)
				
				#recordStr = time.strftime('%H:%M:%S, ')
				recordStr = str(time.time())+', '
				

				for temp in temps:
					recordStr = recordStr + str(temp) + ', '
				for volt in voltages:
					recordStr = recordStr + str(volt) + ', '
							
				recordStr = recordStr.rstrip(', ')

				if fName == None:
					file = sys.stdout
				else:
					file = open(fName,'a')	

				file.write(recordStr+'\n')
				
				if not file == sys.stdout:
					file.close()

				time.sleep(queryPeriod)

		else:
			print 'Failed to connect to SIM922. Try power-cycling.'	
	
	except KeyboardInterrupt:
		print 'Received interrupt - exiting.'
		quit()
	
	except:
		raise
	
	finally:	
		mySim.closeSerial()
		
		if not file == sys.stdout:
			file.close()

