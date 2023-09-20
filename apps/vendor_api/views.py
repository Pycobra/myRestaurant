from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse

from .serializer import VendorSerializer
from apps.vendor.models import Vendor
from apps.order.models import OrderedItemDetail




@api_view(['GET'])
def all_vendor(request):
    if request.method == 'GET':
        data = Vendor.objects.all()
        serializer = VendorSerializer(data, context={'request': request}, many= True)
        return Response(serializer.data)


@api_view(['GET'])
def recent_added_vendor(request):
    if request.method == 'GET':
        data = Vendor.objects.all().order_by('-created_at')[:5]
        serializer = VendorSerializer(data, context={'request': request}, many= True)
        return Response(serializer.data)


@api_view(['GET'])
def best_selling_vendor(request):
    if request.method == 'GET':
        distinct5 = []
        orderDetail = OrderedItemDetail.objects.all().order_by('-quantity')
        # for i in orderDetail: 
        #     if i.product not in distinct5:
        #         distinct5.append(i.product)
        # groupedOrderDetail = OrderedItemDetail.objects.filter(product__in=distinct5[:5])
        order_list = []
        product_list = []
        for ord in orderDetail: 
            if len(order_list)== 0 and len(product_list)== 0:
                product_list.append(ord.product)
                order_list.append(ord)
            elif ord.product in product_list:
                index = product_list.index(ord.product)
                order_list[index].quantity =order_list[index].quantity + ord.quantity
            elif ord.product not in product_list:
                product_list.append(ord.product)
                order_list.append(ord)
        serialized_queryset = serializers.serialize('python', order_list)
        product = {}
        product['ApiResponse'] = serialized_queryset
        # print(serialized_queryset)
        response = JsonResponse(product)
        return response


@api_view(['GET'])
def single_vendor(request, id):
    try:
        vendor = Vendor.objects.get(pk=id)
    except vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = VendorSerializer(vendor, context={'request': request})
        return Response(serializer.data)

