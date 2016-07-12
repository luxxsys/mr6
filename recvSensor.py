#!/usr/bin/python3

import serial,re

tempfile='mr6_tempfile'
humifile='mr6_humifile'
luxfile='mr6_luxfile'
aircfile='mr6_aircfile'
locationfile='mr6_locationfile'
lightfile='mr6_lightfile'

aircstate_old='0'

def compareAircState():
	with open() as hand:
		aircstate_new=hand.read()
		if(aircstate_new==aircstate_old):
			return 0
		else:
			return 1

mys0=serial.Serial('/dev/serial0', 9600, timeout=0.5)

try:
	while True:
		#readline()接收一行数据直到遇到\n，净化、并将bytes解析为str
		recv=mys0.readline().strip()
		print(recv)

		#data example: "HUMI52;TEMP28;LUX1021;"
		#LUX有光为30，无光为1000，浮动两字节，自有长度匹配时才进行处理，否则为废串
		if(len(recv)>=20 and len(recv)<=22): 
			recv=recv.decode('ascii') #收到为bytes，转为str
			load=recv.split(';')
			humidata=re.search(r'HUMI(\d+)', load[0])
#			print(humidata.group(1))
			with open(humifile, 'w') as hand:
				hand.write(humidata.group(1))
	
			tempdata=re.search(r'TEMP(\d+)', load[1])
#			print(tempdata.group(1))
			with open(tempfile, 'w') as hand:
				hand.write(tempdata.group(1))
	
			luxdata=re.search(r'LUX(\d+)', load[2])
#			print(luxdata.group(1))
			with open(luxfile, 'w') as hand:
				hand.write(luxdata.group(1))
except Exception as e:
	print(e)
	mys0.close()
