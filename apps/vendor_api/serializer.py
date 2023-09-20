from rest_framework import serializers
from apps.vendor.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vendor
        fields='__all__'
