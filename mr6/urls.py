"""xxlusite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from smarthome import views as smarthome_views

urlpatterns = [
#	url(r'^admin/', admin.site.urls),
#	url(r'^add(\d+)\+(\d+)$',mr6_iot_views.add,name='add'),
#	url(r'^addd(\d+?)\+(\d+)', mr6_iot_views.add2, name='add2'),
	
	url(r'^$', smarthome_views.getSensor, name='getSensor'),
	#url(r'^setlocation(\d+\.\d+),(\d+\.\d+)$', smarthome_views.setLocation, name='setLocation'),
	url(r'^setlocation$', smarthome_views.setLocation, name='setLocation'),
	url(r'^setstate$', smarthome_views.setState, name='setState'),
	url(r'^log$', smarthome_views.getLocationLog, name='getLocationLog'),

	#url(r'.*', smarthome_views.index, name='default'),
]
