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



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_account(request):
#     if request.method == 'POST':
#         serializer = SignupSerializer(data=request.data)
#         if serializer.is_valid():
#             print('login(request, user)')
#             # serializer.is_active = True
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print(serializer.errors, 'i printed this')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_account(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            # user = serializer.validated_data
            print('--for serializer serializer serializer serializer ||')
            serializer.save()
            return Response(None, status=status.HTTP_201_CREATED)
        print(serializer.errors, 'i printed this')
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

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def tokenObtainPairViewWithUserObject(request):
#     if request.method == 'POST':
#         serializer = MyTokenObtainPairSerializer(data=request.data, context={ 'request': request })
#         if serializer.is_valid():
#             print(serializer, 'i printed this wrongly')
#             return Response(None, status=status.HTTP_202_ACCEPTED)
#         print(serializer.errors, 'i printed this rightly')
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def account(request):
#     if request.method == 'GET':
#         data = UserBase.objects.all()
#         serializer = AccountSerializer(data, context={'request': request}, many= True)
#         return Response(serializer.data)
        

# @api_view(['GET', 'POST'])
# def login_1(request):
#     if request.method == 'POST':
#         serializer = AccountSerializer(data=request.data, context={ 'request': request })
#         if serializer.is_valid(raise_exception=True): #serializer.is_valid(raise_exception=True)
#             print(serializer, "serializerserializer serializerserializer = 666")
#             user = serializer.validated_data['user']
#             login(request, user)
#             return Response(None, status=status.HTTP_202_ACCEPTED)
#         else:
#             print(serializer.errors, "serializerserializer serializerserializer = 44")
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# @api_view(['POST'])
# def login(request):
#     if request.method == 'POST':
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# @api_view(['PUT', 'DELETE'])
# def api_delete_put_acount(request, pk):
#     try:
#         account = UserBase.objects.get(pk=pk)
#     except account.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = AccountSerializer(account, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         account.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PUT'])
# def api_getaccount(request, id):
#     try:
#         account = UserBase.objects.get(pk=id)
#     except account.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = AccountSerializer(account, context={'request': request})
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         serializer = AccountSerializer(account, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






#  elif request.method == 'POST':
        # serializer = AccountSerializer2(data=request.data)
        # if serializer.is_valid():
        #     user = serializer.save()
        #     if user:
        #         token = Token.objects.create(user=user)
        #         json = serializer.data
        #         json['token'] = token.key
        #         return Response(status=status.HTTP_201_CREATED)
            # user = authenticate(
            #     request,
            #     username = serializer['data']['email'],
            #     password = serializer['data']['password']
            # )
            # if user is not None:
            #     login(request, user)
            #     message['key'] = "Successful"
            #     message['value'] = f"{user.user_name} has been logged in"
            #     print("aaaaaaa bbbbbbb ccccccc")
            #     return Response(status=status.HTTP_201_CREATED)
            # else:
            #     message['key'] = "Failed"
            #     message['value'] = "Login Failed Because User Wasn't Authenticated"
            #     print("44444 555555555 666666")
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     print(serializer.errors, 'serializer 555555 6666666666')
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# class VerifyEmail(views.APIView):
#     serializer_class = EmailVeri
#     if request.method == 'GET':
#         content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
#         return Response(content)
# class HomeView(APIView):
#    permission_classes = (IsAuthenticated, )
#    def get(self, request):
#        content = {'message': 'Welcome to the JWT \
#                    Authentication page using React Js and Django!'}
#      return Response(content)
# class VerifyEmail(views.APIView):
#     serializer_class = EmailVerificationSerializer

#     token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
#             user = User.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'email': 'Succesfully activated'}, status = status.HTTP_200_OK)

#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Expired'}, status= status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     pass
    # if request.method == 'POST':
    #     try:
    #         refresh_token = request.data["refresh_token"]
    #         token = RefreshToken(refresh_token)
    #         token.blacklist()
    #         return Response(status=status.HTTP_205_RESET_CONTENT)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#      permission_classes = (IsAuthenticated,)
#      def post(self, request):
#           try:
#                refresh_token = request.data["refresh_token"]
#                token = RefreshToken(refresh_token)
#                token.blacklist()
#                return Response(status=status.HTTP_205_RESET_CONTENT)
#           except Exception as e:
#                return Response(status=status.HTTP_400_BAD_REQUEST)