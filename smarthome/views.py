from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.core.urlresolvers import reverse
from .define import *

def setLocation(request):
	phoneid	= request.GET.get('id','')
	lo = request.GET.get('lo','')
	la = request.GET.get('la','')

	fileRW(locationfile,'a',str(getTimeNow()+'<'+la+','+lo+'<'+phoneid+'\n'))
	#2016-07-05 06:15:49<39.789459,116.557697<70a618c25a2bb852
	return HttpResponse()

def getSensor(request):

	aircmstate=int(fileRW(aircmfile))
	lastestlocation=getLocation()
	if(lastestlocation):
		curLa=float(lastestlocation[1].split(',')[0])
		curLo=float(lastestlocation[1].split(',')[1])
		distance=getDistance(curLa,curLo,tarLa,tarLo)
	if(aircmstate<0):
		aircstate=fileRW(aircfile)
	else:
		aircstate=aircmstate
	if(1==int(aircstate)):
		aircbtn='Off'
		aircstate='On'
	elif(0==int(aircstate)):
		aircbtn='On'
		aircstate='Off'
	else:
		aircbtn=''
		aircstate=''

	lightmstate=int(fileRW(lightmfile))
	if(lightmstate<0):
		lightstate=int(fileRW(lightfile))
	else:
		lightstate=lightmstate
	
	if(1==lightstate):
		lightbtn='Off'
		lightstate='On'
	elif(0==lightstate):
		lightbtn='On'
		lightstate='Off'
	else:
		lightbtn=''
		lightstate=''

	luxanalog=int(fileRW(luxfile))
	if(luxanalog<500):
		luxstate='Good'
	elif(luxanalog>500 and luxanalog<=900):
		luxstate='-'
	elif(luxanalog>900):
		luxstate='Poor'
	else:
		luxstate=''

	data={\
	'distance'		:	'{:.8f}'.format(distance), \
	'temp'			:	fileRW(tempfile), \
	'humi'			:	fileRW(humifile), \
	'lux'			:	luxstate, \
	'light'			:	lightstate,	\
	'airc'			:	aircstate, \
	'lightbtn'		:	lightbtn, \
	'aircbtn'		:	aircbtn	\
	}

	return render(request,'show.html',data)

def setState(request):
	setlightstate=request.GET.get('setlightstate','')
	setaircstate=request.GET.get('setaircstate','')
	autolightstate=request.GET.get('autolight','')
	autoaircstate=request.GET.get('autoairc','')

	if(setlightstate):
		if('On'==setlightstate):
			setlightdigital=1
		elif('Off'==setlightstate):
			setlightdigital=0
		fileRW(lightmfile, 'w',	setlightdigital)
	elif(autolightstate):
		fileRW(lightmfile, 'w',	-1)

	if(setaircstate):
		if('On'==setaircstate):
			setaircdigital=1
		elif('Off'==setaircstate):
			setaircdigital=0
		fileRW(aircmfile, 'w', setaircdigital)
	elif(autoaircstate):
		fileRW(aircmfile, 'w', -1)

	return redirect(reverse('smarthome.views.getSensor', args=[]))
