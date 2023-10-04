import json

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import AccountSerializer, LoginSerializer, SignupSerializer, AddressSerializer, MyTokenObtainPairSerializer

from apps.account.models import UserBase, Address

@api_view(['POST'])
@permission_classes([AllowAny])
def create_account(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TokenObtainPairView alone in thhe url does d work but am doing this 
# class here cos i want to also feed some data along d response
class TokenObtainPairViewWithUserObject(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class BlacklistTokenLogoutView(APIView):
     permission_classes = [AllowAny]
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_address(request):
    if request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        print(request.data, " =====>>>>> request.data")
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_address(request, id):
    if request.method == 'GET':
        data = Address.objects.filter(customer__id=id)
        serializer = AddressSerializer(data, context={'request': request}, many= True)
        return Response(serializer.data)
