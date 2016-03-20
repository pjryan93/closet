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
from models import *
from serializers import *
from rest_framework.renderers import JSONRenderer
import base64, uuid
import cStringIO
import sys
from django.core.files.base import ContentFile
from base64 import b64decode
from django.core.files.images import ImageFile

class HomeView(APIView):
	authentication_classes = (TokenAuthentication,)
	def post(self,request,format=None):
		return  Response({'detail': "I suppose you are authenticated"})
	def get(self,request,format=None):
		print request.user
		return  Response({'detail': "I suppose you are authenticated"})
class CreateCloset(APIView):
	authentication_classes = (TokenAuthentication,)
	def get(self,request,format=None):
		closets = Closet.objects.filter(owner=request.user)
		serializer = ClosetSerializer(closets, many=True)
		json = JSONRenderer().render(serializer.data)
		defaults = DefaultAmounts.objects.filter(current_closet=closets[0].id)
		serializer = ClosetDefaultsSerializer(defaults,many=False)
		json_defaults = JSONRenderer().render(serializer.data)
		print 'here'
		return  Response({'closets': json,'defaults':json_defaults})
	def post(self,request,format=None):
		user = request.user
		print request.data
		print request.data['name']
		print 'done'

		if 'name' in request.data and 'gender' in request.data and 'age' in request.data:
			closetName = request.data['name']
			age = request.data['age']
			gender = request.data['gender']
			cleaned_gender= 'Male'
			if gender == "Male":
				cleaned_gender = "M"
			elif gender == "Female":
				cleaned_gender = "F"
			if 'closet_id' in request.data:
				current_closet = Closet.objects.get(id = request.data["closet_id"])
				current_closet.name = closetName
				current_closet.age = age
				current_closet.sex = gender
				current_closet.save()
				return  Response({'success': "updated",'name':closetName,'id':current_closet.id})
			elif Closet.objects.filter(owner=request.user,name = closetName).count() == 0:
					new_closet = Closet(owner = request.user,name = closetName,age = age,sex = cleaned_gender)
					new_closet.save()
					defaults = DefaultAmounts(current_closet =new_closet )
					defaults.save()
					sizes = DefaultSizes(current_closet=new_closet)
					sizes.setAll(age)
					print 'created'
					return  Response({'success': "created",'name':closetName,'id':new_closet.id})
			else:
				return Response({'failure':'You have a closet with this name'})
		return Response({'failure':'not created'})
class ClosetItem(APIView):
	authentication_classes = (TokenAuthentication,)
	def get(self,request,format=None):
		print request.body
		print request.user
		closets = Closet.objects.filter(owner=request.user)
		if len(closets) == 0:
			defaults = DefaultAmounts()
			serializer = ClosetDefaultsSerializer(defaults,many=False)
			json = JSONRenderer().render(serializer.data)
			return Response({'closets': json,'message':'no closets'})
		else:
			return self.getResponseNoId(request)
		if 'id' in request.GET:
			closets = Closet.objects.filter(owner=request.user)[0]
			serializer1 = ClosetSerializer(closets, many=False)
			json_defaults = JSONRenderer().render(serializer1.data)
			defaults = DefaultAmounts.objects.filter(current_closet=closets.id)
			serializer = ClosetDefaultsSerializer(defaults,many=True)
			json = JSONRenderer().render(serializer.data)
			clothing_items = ClothingItem.objects.filter(current_closet=closets.id)
			item_serializer = ItemSerializer(clothing_items,many=True)
			item_json = JSONRenderer().render(item_serializer.data) 
			size_defaults= DefaultSizes.objects.filter(current_closet=closets.id)
			if len(size_defaults) == 0:
				default_size = DefaultSizes(current_closet = closets)
				default_size .save()
				size_defaults= DefaultSizes.objects.filter(current_closet=closets.id)
			size_serializer = ItemSizeSerializer(size_defaults,many=True)
			size_json = JSONRenderer().render(size_serializer.data) 
			print 'size_json'
			print size_json
			return  Response({'closets': json, 'defaults':json_defaults,'items':item_json,'sizes':size_json,'message':'success'})
	def getResponseNoId(self,request):
		closets = Closet.objects.filter(owner=request.user)[0]
		serializer1 = ClosetSerializer(closets, many=False)
		json_defaults = JSONRenderer().render(serializer1.data)
		defaults = DefaultAmounts.objects.filter(current_closet=closets.id)
		serializer = ClosetDefaultsSerializer(defaults,many=True)
		json = JSONRenderer().render(serializer.data)
		clothing_items = ClothingItem.objects.filter(current_closet=closets.id)
		item_serializer = ItemSerializer(clothing_items,many=True)
		item_json = JSONRenderer().render(item_serializer.data) 
		size_defaults= DefaultSizes.objects.filter(current_closet=closets.id)
		if len(size_defaults) == 0:
			default_size = DefaultSizes(current_closet = closets)
			default_size .save()
			size_defaults= DefaultSizes.objects.filter(current_closet=closets.id)
		size_serializer = ItemSizeSerializer(size_defaults,many=True)
		size_json = JSONRenderer().render(size_serializer.data) 
		print 'size_json'
		print size_json
		return  Response({'closets': json, 'defaults':json_defaults,'items':item_json,'sizes':size_json,'message':'success'})
	def post(self,request,format=None):
		item_name = request.data['name']
		item_type = request.data['type']
		item_size = request.data['size']
		closet_id = request.data['closet_id']
		photoDataString = request.data['photoData']
		image_output = cStringIO.StringIO()
		image_output.write(photoDataString.decode('base64'))
		image_output.read()
		image_output.seek(0)    # Write decoded image to buffer
		current_closet = Closet.objects.get(id=closet_id)
		x = ClothingItem(name=item_name,clothing_type = item_type,size=item_size,current_closet=current_closet)
		file_name = str(x.id) + '.png'
		image_data = b64decode(photoDataString)
		uploadedImage = ContentFile(image_data,file_name)
		print uploadedImage
		x.save()
		x.item_image = uploadedImage
		x.save()
		print x.id
		return  Response({'failure': 'no id' })