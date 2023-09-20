from rest_framework import serializers
from .models import *


class CategorySerialized(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class ProductSerialized(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = '__all__'




    