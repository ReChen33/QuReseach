#!/usr/bin/python

import sys, os
import time
from simInterface import simInterface
import numpy as np
import csv


queryPeriod = 0.3 #time in seconds between polls to the sim

AC_PORT = sys.argv[1]  #port on the SRS box is first argument (after script name) in command line
channel=sys.argv[2]    # channel (curve) is second argument (1,2,3)
curvename=sys.argv[3]   #curve name is third argument
fName = sys.argv[4]    # cal file is fourth argument 
calarray=np.loadtxt(fName, delimiter='\t')       #load in cal array from file
print fName
mySim = simInterface()
mySim.connectToSimPort(AC_PORT)
try:
		if mySim.getDeviceID() == 'SIM921': #SIM921 is the ac resistance bridge
			mySim.write('CINI 2,0,interhead')
			time.sleep(queryPeriod)
			for index in range(len(calarray)):
				#print index
				temppoint=calarray[index,0]
				#print temppoint
				voltpoint=calarray[index,1]
				print index, voltpoint, temppoint
				time.sleep(queryPeriod)
				mySim.write('CAPT 2,{0},{1}'.format(voltpoint,temppoint))
				#mySim.addCalPoint(voltpoint, temppoint)
				time.sleep(queryPeriod)
				output3=mySim.query('CAPT? 2,{0}'.format(index))
				print output3

			mySim.write('CURV 2')
			output2=mySim.query('CURV?')
			print output2
			output=mySim.query('CINI? 2')
			print output

		else:
			print 'Failed to connect to SIM922. Try power-cycling.'	
	
except KeyboardInterrupt:
	print 'Received interrupt - exiting.'
	quit()
	
except:
	raise
	
finally:	
	mySim.closeSerial()
		
	
