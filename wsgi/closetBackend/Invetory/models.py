# Create your models here.
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Closet(models.Model):
	owner = models.ForeignKey(User, related_name='creater')
	name = models.CharField(max_length = 40,default = 'new closet') 
	sex =  models.CharField(max_length = 7,default = 'N')
	age =  models.CharField(max_length = 3,default = '0') 
class DefaultAmounts(models.Model):
	 current_closet = models.OneToOneField(Closet,on_delete=models.CASCADE)
	 tops = models.IntegerField(default = 10)
	 bottoms = models.IntegerField(default = 14)
	 socks  = models.IntegerField(default = 14)
	 shoes = models.IntegerField(default = 3)
	 dress_cloths = models.IntegerField(default = 4)
	 underwear = models.IntegerField(default = 14)
	 swimwear = models.IntegerField(default = 2)
	 outerwear = models.IntegerField(default = 2)
	 onsies = models.IntegerField(default = 14)
	 pajamas = models.IntegerField(default = 10)
STANDARD_CHOICES = (
		('P', 'P'),
		('NB', 'NB'),
		('3M','3M'),
		('6M','6M'),
		('9M','9M'),
		('12M','12M'),
		('18M','18M'),
		('24M','24M'),
		('2T','2T'),
		('3T','3T'),
		('4T','4T'),
		('5T','5T'),
		('3.5','3.5'),
		('4','4'),
		('4','4.5'),
		('5','5'),
		('5.5','5.5'),
		('6','6'),
		('6.5','6.5'),
		('7','7'),
		('7.5','7.5'),
		('8','8'),
		('8.5','8.5'),
		('9','9'),
		('9.5','9.5'),
		('10','10')
)
class DefaultSizes(models.Model):
	 current_closet = models.OneToOneField(Closet,on_delete=models.CASCADE)
	 tops = models.CharField(max_length = 3,default = 'NB' ,choices=STANDARD_CHOICES) 
	 bottoms = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 socks  = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 shoes = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 dress_cloths = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 underwear = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 swimwear = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 outerwear = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 onsies = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES) 
	 pajamas = models.CharField(max_length = 3,default = 'NB',choices=STANDARD_CHOICES)
	 def setAll(self,value):
		self.tops = value
		self.bottoms = value
		self.socks = value
		self.shoes = value
		self.dress_cloths = value
		self.underwear = value
		self.swimwear = value
		self.outerwear = value
		self.onsies = value
		self.pajamas = value 
		self.save()
def image_path(instance,filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return 'item_{0}'.format(instance.id)
class ClothingItem(models.Model):
	current_closet = models.ForeignKey(Closet, related_name='current_closet')
	clothing_type = models.CharField(max_length = 40,default = 'new closet')
	size = models.CharField(max_length = 4,default = 'm')
	name = models.CharField(max_length=30,default = "no name")
	season = models.CharField(max_length=20,default = 'all')
	sex = models.CharField(max_length=1,default = 'N')
	item_image = models.ImageField(upload_to=image_path, blank=True, null=True)
