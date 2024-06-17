import time
import serial
import glob
import sys

def serialPorts():
    #only for Linux
    if sys.platform.startswith('linux'):
        ports = glob.glob('/dev/tty[USB]*')
    else:
        raise EnvironmentError('Not Linux')
    result = None
    for port in ports:
        try:
            s = serial.Serial(port)
            time.sleep(0.1)
            s.write('Version')
            time.sleep(0.1)
            waitMsg = s.inWaiting()
            msg = s.read(waitMsg)
            #print(msg)
            if msg == "TEMPerX232_V2.5\r\n":
                result = port
                break

        except (OSError,serial.SerialException):
            pass
    return result

if __name__ == '__main__':
    print(serialPorts())


