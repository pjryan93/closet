from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
	 url(r'^invetory/',HomeView.as_view(),name = 'auth-view'),
	 url(r'^create/',CreateCloset.as_view(),name = 'create-view'),
	 url(r'^closet/',ClosetItem.as_view(),name = 'create-view')
]