from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
class AuthView(APIView):
    """
    Authentication is needed for this methods
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        print request
        print request.body
        return Response({'detail': "I suppose you are authenticated"})
class HomeView(APIView):
	def POST(self,request,format=None):
		return  Response({'detail': "I suppose you are authenticated"})
def tester(request):
	print request.user
	print request.GET
	return HttpResponse(status=200)