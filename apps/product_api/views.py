import json


from django.http import JsonResponse
from django.core import serializers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .serializer import CategorySerializer, ProductSerializer
from apps.product.models import Product, Category
from apps.vendor.models import Vendor
from apps.order.models import OrderedItemDetail




@api_view(['GET'])
def all_category(request):
    if request.method == 'GET':
        data = Category.objects.all()
        serializer = CategorySerializer(data, context={'request': request}, many= True)
        return Response(serializer.data)
@api_view(['GET'])
def single_category(request, id):
    try:
        category = Category.objects.get(pk=id)
    except category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)


# ===============================Product============================

@api_view(['GET'])
def all_product(request):
    if request.method == 'GET':
        data = Product.objects.all()

        recent = Product.objects.all().order_by('-created_at')[:6]
        serializer = ProductSerializer(data, context={'request': request}, many= True)
        serializer_recent = ProductSerializer(recent, context={'request': request}, many= True)
        return Response(serializer.data)#, serializer_recent.data)
@api_view(['GET'])
def recent_product(request):
    if request.method == 'GET':
        recent = Product.objects.all().order_by('-created_at')[:6]
        serializer = ProductSerializer(recent, context={'request': request}, many= True)
        return Response(serializer.data)#, serializer_recent.data)
@api_view(['GET'])
def best_selling_product(request):
    if request.method == 'GET':
        distinct5 = []
        orderDetail = OrderedItemDetail.objects.all().order_by('-quantity')
        for i in orderDetail: 
            if i.product not in distinct5:
                distinct5.append(i.product)
        groupedOrderDetail = OrderedItemDetail.objects.filter(product__in=distinct5[:5])
        order_list = []
        product_list = []
        for ord in groupedOrderDetail: 
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
        response = JsonResponse(product)
        return response

@api_view(['GET'])
def single_product(request, str, id):
    try:
        if str == "shop":
            product = Product.objects.get(pk=id)
        elif str == "vendor-shop":
            product = Product.objects.get(vendor__id=id)
    except product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
@api_view(['GET'])
def all_vendor_product(request):
    if request.method == 'GET':
        data = Vendor.objects.all()
        useData = [vendor.vendors_products.all() for vendor in data]
        serialized_queryset = [serializers.serialize('python', obj) for obj in useData]
        # serialized_queryset = [{'vendor': serializers.serialize('python', vendor), 'detail': [serializers.serialize('python', obj) for obj in useData]} for vendor in data]
        product = {}
        product['ApiResponse'] = serialized_queryset
        response = JsonResponse(product)
        return response