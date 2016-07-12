#!/usr/bin/python3
import serial

aircstate=''
msgon = b'00001001:00KT:01:0001'
msgoff= b'00001001:00KT:01:0000'

with open(aircfile, 'r') as hand:
	aircstate=hand.read()
mys0 = serial.Serial('/dev/serial0', 9600, timeout=0.8)

if('0'==aircstate):
	mys0.write(msgoff)
elif('1'==aircstate):
	mys0.write(msgon)

try:
	while True:
		reply = mys0.read(3).decode()
		if(reply=='OK'):
			print('OK')
			break
		elif(reply=='NOK'):
			print('NOK')
			break
		else:
		 	print('Err:'+reply)
		 	break
		 	
except KeyboardInterrupt:
	mys0.close()
