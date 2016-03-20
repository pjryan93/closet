from rest_framework.serializers import ModelSerializer,  SerializerMethodField
from models import *

class ClosetSerializer(ModelSerializer):
    class Meta:
        model = Closet
        fields = ('id', 'name','age','sex')
class ClosetDefaultsSerializer(ModelSerializer):
    class Meta:
        model = DefaultAmounts
class ItemSerializer(ModelSerializer):
    class Meta:
        model = ClothingItem
        fields = ('clothing_type','size','name','season','sex','item_image')
    def get_item_image(self, obj):
        return obj.image.url
class ItemSizeSerializer(ModelSerializer):
    class Meta:
        model = DefaultSizes


