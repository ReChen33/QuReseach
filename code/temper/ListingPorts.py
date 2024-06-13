import sys
import glob
import serial
import time


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = None
    """#Problem may happen to loop
        as it will send to all port a command 'Version' and wait for data
    """
    for port in ports:
        try:
            s = serial.Serial(port)
            s.write('Version'.encode())
            time.sleep(0.1)
            bytesToRead = s.inWaiting()
            msg = s.read(bytesToRead).decode()
            #print(msg)
            time.sleep(0.1)

            if msg == "TEMPerX232_V2.5\r\n":
                result = port
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    print(type(serial_ports()),serial_ports())

