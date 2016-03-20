from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
	 url(r'^tester/',AuthView.as_view(),name = 'auth-view')
]