#!/usr/bin/python3
import serial,re,time

low=b'00001001:00DD:01:0001'
high=b'00001001:00DD:01:0000'

mys0=serial.Serial('/dev/serial0', 9600, timeout=0.5)

while True:
	try:
		sig = int(input("Control MSG: "))
		if 1==sig:
			mys0.write(high)
		elif 0==sig:
			mys0.write(low)
		else:
			print('bad msg')
	except Exception as e:
		print(e)
		mys0.close()
