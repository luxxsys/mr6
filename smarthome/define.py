from math import *
import time

tempfile='/home/pi/mr6/mr6_tempfile'
humifile='/home/pi/mr6/mr6_humifile'
luxfile='/home/pi/mr6/mr6_luxfile'
aircfile='/home/pi/mr6/mr6_aircfile'
aircmfile='/home/pi/mr6/mr6_aircmfile'
locationfile='/home/pi/mr6/mr6_locationfile'
lightfile='/home/pi/mr6/mr6_lightfile'
lightmfile='/home/pi/mr6/mr6_lightmfile'
distancefile='/home/pi/mr6/mr6_distancefile'
logfile='/home/pi/mr6/mr6_log'

tarLa=39.798968061371966
tarLo=116.56022590695919
#谷歌地图：39.8000607119,116.5659847136
#百度地图：39.8057960000,116.5725510000
#腾讯高德：39.8000702378,116.5659979845
#图吧地图：39.8003791578,116.5554796845
#谷歌地球：39.7989891578,116.5601696845
#北纬N39°47′56.36″ 东经E116°33′36.61″

def getTimeNow():
	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def fileRW(myfile, method='r',content=None):
	content=str(content)
	if('r'==method):
		with open(myfile, 'r') as hand:
			return hand.read()
	if('rl'==method):
		with open(myfile, 'r') as hand:
			return hand.readlines()
	elif('w'==method):
		with open(myfile, 'w') as hand:
			return hand.write(content)
	elif('a'==method):
		with open(myfile, 'a') as hand:
			return hand.write(content)

def getLocation():
	locationlines=fileRW(locationfile, 'rl')
	if(locationlines):
		lastestlocation=locationlines[-1]
		return lastestlocation.split('<')
	else:	
		return ''

# output distance 距离(km)
def getDistance():
	lastestlocation=getLocation()
	Lat_A=float(lastestlocation[1].split(',')[0])
	Lng_A=float(lastestlocation[1].split(',')[1])
	Lat_B=tarLa
	Lng_B=tarLo

	ra = 6378.140  # 赤道半径 (km)
	rb = 6356.755  # 极半径 (km)
	flatten = (ra - rb) / ra  #地球扁率
	rad_lat_A = radians(Lat_A)
	rad_lng_A = radians(Lng_A)
	rad_lat_B = radians(Lat_B)
	rad_lng_B = radians(Lng_B)
	pA = atan(rb/ra*tan(rad_lat_A))
	pB = atan(rb/ra*tan(rad_lat_B))
	xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
	c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
	c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
	dr = flatten / 8 * (c1 - c2)
	distance = ra * (xx + dr)
	return distance

def getClientIP(request):
	if 'HTTP_X_FORWARDED_FOR' in request.META:
		return request.META['HTTP_X_FORWARDED_FOR']
	else:
		return request.META['REMOTE_ADDR']
