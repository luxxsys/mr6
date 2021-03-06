#!/usr/bin/python3
import serial,re,time
from smarthome.define import fileRW,getDistance

tempfile='mr6_tempfile'
humifile='mr6_humifile'
luxfile='mr6_luxfile'
aircfile='mr6_aircfile'
aircmfile='mr6_aircmfile'
locationfile='mr6_locationfile'
lightfile='mr6_lightfile'
lightmfile='mr6_lightmfile'
distancefile='mr6_distancefile'

aircstate_old=0
lightstate_old=0
IRP_TTL=IRP_TTL_init=180

def setAirc(serial, state, times=1):
	global aircstate_old
	state=int(state)
	i=0
	msg_on=b'00001001:00KT:01:0001'
	msg_off=b'00001001:00KT:01:0000'
	msg_unSwing=b'00001001:00KT:01:0002'
	if(state!=aircstate_old):
		if(1==state):
			for i in range(0,times):
				serial.write(msg_on)
				time.sleep(1.5)
		if(0==state):
			for i in range(0,times):
				serial.write(msg_off)
				time.sleep(1.5)
		if(2==state):
			for i in range(0,times):
				serial.write(msg_unSwing)
				time.sleep(1.5)
		aircstate_old=state

def setLight(serial, state, times=1):
	global lightstate_old
	state=int(state)
	i=0
	msg_on=b'00001001:00DD:01:0000'
	msg_off=b'00001001:00DD:01:0001'
	if(state!=lightstate_old):
		if(1==state):
			#print('hereon')
			for i in range(0,times):
				serial.write(msg_on)
				time.sleep(0.5)
		if(0==state):
			#print('hereoff')
			for i in range(0,times):
				serial.write(msg_off)
				time.sleep(0.5)
		lightstate_old=state

mys0=serial.Serial('/dev/serial0', 9600, timeout=0.5)

while True:
	try:
		aircmstate=int(fileRW(aircmfile))
		aircstate=int(fileRW(aircfile))
		lightmstate=int(fileRW(lightmfile))
		lightstate=int(fileRW(lightfile))
		lux=int(fileRW(luxfile))

		if(aircmstate<0):
			distance=getDistance()
			if(distance*1000<500):
				fileRW(aircfile,'w',1)
			else:
				fileRW(aircfile,'w',0)
			setAirc(mys0,aircstate,3)
		else:
			setAirc(mys0,aircmstate,3)

		if(lightmstate>=0):
			setLight(mys0,lightmstate,3)
			IRP_TTL=0
		elif(lightmstate<0):
			setLight(mys0,lightstate,3)


		#温湿度、光线参数提取
		#readline()接收一行数据直到遇到\n，净化、并将bytes解析为str
		recv=(mys0.readline().strip()).decode('ascii')
		#print(len(recv))
		print(recv)
		
		#data example: "HUMI52;TEMP28;LUX1021;"
		#LUX有光为30，无光为1000，浮动两字节，自有长度匹配时才进行处理，否则为废串
		if(8==len(recv) or 6==len(recv)):
			load=recv.split(';')

			#humidata=re.search(r'HUMI(\d+)', load[0])
			#fileRW(humifile, 'w', humidata.group(1))
			#print(humidata.group(1))
			#tempdata=re.search(r'TEMP(\d+)', load[1])
			#fileRW(tempfile, 'w', tempdata.group(1))
			#print(tempdata.group(1))
			luxdata=re.search(r'LUX(\d+)', load[0])
			fileRW(luxfile, 'w', luxdata.group(1))
			#print(luxdata.group(1))

		elif('IRPACTIVE'==recv and lightmstate<0):
			if(lux>500):
				#print(lux)
				fileRW(lightfile,'w',1)
			elif(lux<500):
				fileRW(lightfile,'w',0)
				continue
			IRP_TTL=IRP_TTL_init
			print(IRP_TTL)
		else:
			if(lux<500):
				fileRW(lightfile,'w',0)
				continue
			IRP_TTL-=1
			print(IRP_TTL)
			if(0==IRP_TTL):
				fileRW(lightfile,'w',0)
			elif(IRP_TTL<0):
				IRP_TTL=0
	except Exception as e:
		print(e)
		continue
