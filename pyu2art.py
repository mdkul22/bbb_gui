import serial
ser = serial.Serial(port='dev/ttyACM0',baudrate= 9600,timeout=1)

def readr():
	try:
		return  ser.read()
	
	except (NoneType, RuntimeError):
		pass

def checkr(value):
		 
