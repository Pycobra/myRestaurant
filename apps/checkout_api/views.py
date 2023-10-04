import json


from django.http import JsonResponse
from django.core import serializers
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .serializer import PaymentVerificationDataSerializer, DeliveryOptionsSerializer, PaymentSelectionsSerializer, OrderRecieptSerializer, OrderedItemDetailSerializer
from apps.checkout.models import DeliveryOptions, PaymentSelections


@api_view(['GET'])
def delivery_options(request):
    if request.method == 'GET':
        data = DeliveryOptions.objects.all()
        serializer = DeliveryOptionsSerializer(data, context={'request': request}, many= True)
        return Response(serializer.data)

@api_view(['GET'])
def payment_selections(request):
    if request.method == 'GET':
        data = PaymentSelections.objects.all()
        serializer = PaymentSelectionsSerializer(data, context={'request': request}, many= True)
        return Response(serializer.data)


@api_view(['GET'])
def paystack_public_key(request):
    if request.method == 'GET':
        key = settings.PAYSTACK_PUBLIC_KEY
        return Response(key)
@api_view(['GET'])
def flutterwave_public_key(request):
    if request.method == 'GET':
        key = settings.FLUTTERWAVE_PUBLIC_KEY
        return Response(key)

@api_view(['POST'])
def complete_payment(request):
    if request.method == 'POST':
        # payment_name = request.data['payment_name']
        # if payment_name == "flutterwave-payment":
        #     ref =  request.data['tx_ref']
        # elif payment_name == "paystack-payment":
        #     ref =  request.data['ref']
        orderReciept_serializer = OrderRecieptSerializer(data=request.data)
        if orderReciept_serializer.is_valid(raise_exception=True):
            orderReciept = orderReciept_serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        elif orderReciept_serializer.errors:
            return Response(orderReciept_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


