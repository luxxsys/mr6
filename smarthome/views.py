from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.core.urlresolvers import reverse
from .define import *

def getLocationLog(request):
	lines=fileRW(locationfile, 'rl')
	response=HttpResponse()
	for line in lines[-5:]:
		response.write(line+'<br/>')
	return response

def setLocation(request):
	phoneid	= request.GET.get('id','')
	lo = request.GET.get('lo','')
	la = request.GET.get('la','')

	fileRW(locationfile,'w',str(getTimeNow()+'<'+la+','+lo+'<'+phoneid+'\n'))
	#2016-07-05 06:15:49<39.789459,116.557697<70a618c25a2bb852
	fileRW(distancefile, 'w', str(getDistance()))
	return HttpResponse()

def getSensor(request):

	distance=getDistance()

	aircmstate=int(fileRW(aircmfile))
	if(aircmstate<0):
		aircstate=fileRW(aircfile)
	else:
		aircstate=aircmstate
	if(1==int(aircstate)):
		aircbtn='Off'
		aircstate='On'
		aircswingbtn='unSwing'
	elif(0==int(aircstate)):
		aircbtn='On'
		aircstate='Off'
		aircswingbtn='unSwing'
	elif(2==int(aircstate)):
		aircbtn='Off'
		aircstate='On'
		aircswingbtn='Swing'
	else:
		aircbtn=''
		aircstate=''
		aircswingbtn=''

	lightmstate=int(fileRW(lightmfile))
	print(lightmstate)
	if(lightmstate<0):
		lightstate=int(fileRW(lightfile))
	else:
		lightstate=lightmstate
	print(lightstate)
	
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

	clientip=getClientIP(request)

	data={\
	'distance'		:	'{:.8f}'.format(distance),\
	'temp'			:	fileRW(tempfile),\
	'humi'			:	fileRW(humifile),\
	'lux'			:	luxstate,\
	'light'			:	lightstate,\
	'airc'			:	aircstate,\
	'lightbtn'		:	lightbtn,\
	'aircbtn'		:	aircbtn,\
	'clientip'		:	clientip,\
	'aircswingbtn'		:	aircswingbtn\
	}

	return render(request,'show.html',data)

def setState(request):
	clientip=getClientIP(request)
	setlightstate=request.GET.get('setlightstate','')
	autolightstate=request.GET.get('autolight','')
	setaircstate=request.GET.get('setaircstate','')
	autoaircstate=request.GET.get('autoairc','')
	setaircswing=request.GET.get('swing','')

	if(setlightstate):
		if('On'==setlightstate):
			setlightdigital=1
		elif('Off'==setlightstate):
			setlightdigital=0
		fileRW(lightmfile, 'w',	setlightdigital)
		fileRW(logfile, 'a', getTimeNow()+'>'+clientip+'>set_light_to>'+str(setlightdigital)+'\n')
	elif(autolightstate):
		fileRW(lightmfile, 'w',	-1)
		fileRW(logfile, 'a', getTimeNow()+'>'+clientip+'>set_light_to>auto'+'\n')
	elif(setaircstate):
		if('On'==setaircstate):
			setaircdigital=1
		elif('Off'==setaircstate):
			setaircdigital=0
		fileRW(aircmfile, 'w', setaircdigital)
		fileRW(logfile, 'a', getTimeNow()+'>'+clientip+'>set_airc_to>'+str(setaircdigital)+'\n')
	elif(setaircswing):
		if('Swing'==setaircswing):
			setaircdigital=1
		elif('unSwing'==setaircswing):
			setaircdigital=2
		fileRW(aircmfile, 'w', setaircdigital)
		fileRW(logfile, 'a', getTimeNow()+'>'+clientip+'>set_airc_to>'+str(setaircdigital)+'\n')
	elif(autoaircstate):
		fileRW(aircmfile, 'w', -1)
		fileRW(logfile, 'a', getTimeNow()+'>'+clientip+'>set_airc_to>auto'+'\n')

	return redirect(reverse('smarthome.views.getSensor', args=[]))
