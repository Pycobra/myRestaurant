from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.account.models import UserBase, Address
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import re

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserBase
        fields=("id", 'user_name', 'email', 'password', "unique_id",
                "firstname", "surname", "user_image", "mobile",
                "is_active", "is_staff", "created_at", "updated_at")
                
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise AuthenticationFailed('Access denied: wrong username or password.')
                # raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise AuthenticationFailed('Both "username" and "password" are required.')
            # raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    # def create(self, validated_data):
    #     # password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
        
    #     # print('--for instance instance instance instance ||')
    #     # if password is not None:
    #     #     instance.set_password(password)
    #     # instance.is_active = True
    #     instance.save()
    #     return instance

    


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserBase
        fields=('email', 'user_name', 'password', 'is_active')
        exra_kwargs= {'password':{'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        print('--for instance instance instance instance ||')
        if password is not None:
            instance.set_password(password)
        instance.is_active = True
        instance.save()
        return instance

    def validate_password(self, password):
        password2 =self.initial_data.get('password2')
        contains_characters = re.search(r"\W", password)
        contains_digit = re.search(r"\d", password)
        contains_white_space = re.search(r"\s", password)      
        if len(password) >= 8:
            if contains_characters == None:
                raise serializers.ValidationError("Password must include characters")
            elif contains_digit == None:
                raise serializers.ValidationError("Password must include digits")
            elif contains_white_space != None:
                raise serializers.ValidationError("Password allows no white space")
            elif password != password2:
                raise serializers.ValidationError("Both passwords do not match")
        else:
            raise serializers.ValidationError("password must be longer than 8 characters")
        return password

    def validate_user_name(self, user_name):
        contains_characters = re.search(r"\W", user_name)
        if len(user_name) >= 4:
            if contains_characters != None:
                raise serializers.ValidationError("Username cannot include characters")
        else:
            raise serializers.ValidationError("Username must be 4 or more characters")

        return user_name

    def validate_email(self, email):
        new_email = UserBase.objects.filter(email__exact=email)
        if new_email.exists():
            raise serializers.ValidationError("Email already taken, please use another Email")
        else:
            contain_unwanted_characterz =False
            #checks & executes if it contains characters
            contains_characters = re.search(r"\W", email)
            if contains_characters != None:
                unwanted_characterz = ['~', '!', '#', '$', '%', '^', '&', '*', '(', ')', \
                             '+', '=', '[', ']', '{', '}', '|', '', ":", ";", '"', "'", \
                               '<', ",", '>', "?"]

                for i in email:
                    if i in unwanted_characterz:
                        contain_unwanted_characterz =True
                        break
            if contain_unwanted_characterz == True:
                raise serializers.ValidationError("Email contains unwanted character")

            # checks & executes if it doesnt contains characters at all / bad character
            elif contain_unwanted_characterz == False:
                ends_with = re.search(r'@yahoo.com$|gmail.com$|hotmail.com$', email)
                if ends_with != None:
                    pass
                else:
                    raise serializers.ValidationError("invalid email pattern, must end with [gmail.com, yahoo.com etc]")
        return email
        
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['user_name'] = user.user_name
        token['email'] = user.email
        token['password'] = user.password
        token['unique_id'] = user.unique_id
        token['is_active'] = user.is_active
        token['is_staff'] = user.is_staff
        return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     refresh = self.get_token(self.user)
    #     email = attrs.get('email')
    #     password = attrs.get('password')
    #     print(email, password)
    #     if email and password:
    #         # Try to authenticate the user using Django auth framework.
    #         user = authenticate(request=self.context.get('request'),
    #                             email=email, password=password)
    #         print(user, "didnt run this")
    #         if not user:
    #             raise serializers.ValidationError('Access denied: wrong username or password.')
    #             # raise serializers.ValidationError('Access denied: wrong username or password.', code='authorization')
    #     else:
    #         raise serializers.ValidationError('Both "username" and "password" are required.')
    #         # raise serializers.ValidationError('Both "username" and "password" are required.', code='authorization')

    #     return data


