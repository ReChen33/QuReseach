import serial
import time


devicePort = '/dev/ttyUSB0' #USB to serial device
escapeString = 'xYz' #some random string of letters that won't ever look like a command
serialBaudRate = 9600 #default for the 922
serialTimeout = 1

responseWaitTime = 0.25 #seconds

class simInterface:

	def __init__(self):

		self.devicePort = devicePort
		self.escapeString = escapeString
		self.serialBaudRate = serialBaudRate
		self.serialTimeout = serialTimeout
		
		self.verbose = False
		
		self.confSerial()
		self.openSerial()
	
		
	def confSerial(self):
							
		self.sim = serial.Serial()
		self.sim.port = self.devicePort
		self.sim.baudrate = self.serialBaudRate
		self.sim.timeout = self.serialTimeout
		
		if self.sim.isOpen():
			self.closeSerial()
		
	def openSerial(self):
		self.sim.open()
		self.sim.write('CONS OFF') #turn console mode off incase it's on
		self.sim.write(self.escapeString)
		self.getFullDeviceID()

	def closeSerial(self):
		self.sim.close()
	
	def connectToSimPort(self, port):
		self.write('CONN {0}, "{1}"'.format(port, self.escapeString))
		time.sleep(responseWaitTime)

	def flushOutput(self):
		self.write('FLSO')	
		
	def write(self,message):
		message = message + '\r\n'
		self.sim.write(message)
		if self.verbose:
			print message
			
	def readline(self):
		return self.sim.readline()	
	
	def getDeviceID(self):
		id = self.getFullDeviceID()
		try:
			return id.split(',')[1]
		except IndexError:
			return 'None'
	
	def getFullDeviceID(self):	
		return self.query('*IDN?')

	def initDiodeCal(self, channel,curvename):
		self.write('CINI {0},0,"{1}"'.format(channel,curvename))

	def queryDiodeCal(self,channel):
		return self.query('CINI? {0}'.format(channel))

	def addCalPoint(self, voltpoint, temppoint):
		self.write('CAPT 4,{0},{1}'.format(voltpoint, temppoint))

	def queryCalPoint(self, calpoint):
		return self.query('CAPT? 4,{0}'.format(calpoint))

	def selectCalCurve(self, channel):    #curve can be 'STAN 0' or 'USER 1'
		self.write('CURV {0},1'.format(channel))

	def queryCalCurve(self, channel):
		return self.query('CURV? {0}'.format(channel))

	def query(self, message):
		self.write(message)
		time.sleep(responseWaitTime)
		return self.readline().rstrip()
	
	def getVoltages(self):
		volts = self.query('VOLT? 0,1')
		volts = volts.split(',')
		try:
			voltages = map(float, volts)
		except ValueError:
			voltages = [float('nan')]	
		return voltages
		
	def getTemps(self):
		temps = self.query('TVAL? 0,1')			
		temps = temps.split(',')
		try:
			temperatures = map(float,temps)
		except ValueError:
			temperatures = [float('nan')]
		return temperatures		
	def switchMUX(self,channel):
		self.write('CHAN {0}'.format(channel))

	def setCalCurveAC(self,channel):
		self.write('CURV {0}'.format(channel))

	def queryCalCurveAC(self):
		return self.query('CURV?')

	def getTempAC(self):
		temp = self.query('TVAL?')
		return temp
		
