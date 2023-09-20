from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.template.context_processors import request
from django.contrib.auth.password_validation import validate_password

import re

from apps.order.models import Address
from .models import UserBase



class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Username', min_length=4,  max_length=50, help_text='Required')
    email = forms.EmailField(label='Email', max_length=100, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    class Meta:
        model= UserBase
        fields=('user_name', 'email', 'password', 'password2')

    def clean_username(self):
        # user_name = self.cleaned_data['user_name'].lower()
        # exists= UserBase.objects.filter(user_name=user_name)
        # if exists.count():
        #     raise forms.ValidationError("Username already exists")
            
        user_name = self.cleaned_data['user_name'].lower()
        new_username = UserBase.objects.filter(user_name__exact=user_name)
        if new_username.exists():
            raise forms.ValidationError("Username already exists")
        else:
            if len(user_name) >= 4:
                if contains_characters != None:
                    raise forms.ValidationError("Username cannot include characters")
                else:
                    raise forms.ValidationError("")
            else:
                raise forms.ValidationError("Username must be 4 or more characters")

        return user_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new_email = UserBase.objects.filter(email__exact=email)
        if new_email.exists():
            raise forms.ValidationError("Email already taken, please use another Email")
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
                raise forms.ValidationError("Email contains unwanted character")

            # checks & executes if it doesnt contains characters at all / bad character
            elif contain_unwanted_characterz == False:
                ends_with = re.search(r'@yahoo.com$|gmail.com$|hotmail.com$', email)
                if ends_with != None:
                    pass
                else:
                    raise forms.ValidationError("invalid email pattern, must end with [gmail.com, yahoo.com etc]")
        return email

    def clean_password2(self):
        password2 = self.cleaned_data['password2'].lower()
        # password = self.cleaned_data['password'].lower()
        password = self.non_cleaned_password
                
        if password != password2:
            raise forms.ValidationError("Both passwords do not match")
        return password2

    def clean_password(self):
        password = self.cleaned_data['password'].lower()
        self.non_cleaned_password = password
        contains_characters = re.search(r"\W", password)
        contains_digit = re.search(r"\d", password)
        contains_white_space = re.search(r"\s", password)      
        if len(password) >= 8:
            if contains_characters == None:
                raise forms.ValidationError("Password must include characters")
            if contains_digit == None:
                raise forms.ValidationError("Password must include digits")
            if contains_white_space != None:
                raise forms.ValidationError("Password allows no white space")
            else:
                pass
        else:
            raise forms.ValidationError("password must be longer than 8 characters")
        return password

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.non_cleaned_password = None
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Username', 'id': 'signup-username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Email', 'name': 'email', 'id': 'signup-email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'password', 'id': 'signup-pwd'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Repeat Password', 'id': 'signup-pwd2'})

class UserLoginForm(forms.ModelForm):
    email_as_username = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-input', 'name': "email_as_username", 'placeholder': 'Email', 'id': 'login-email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
            attrs={'class': 'form-input', 'name': "password", 'placeholder': 'Password', 'id': 'login-pwd'}))

    class Meta:
        model= UserBase
        fields=('email_as_username', 'password')

    def clean_email_as_username(self):
        email_as_username = self.cleaned_data['email_as_username'].lower()
        user= UserBase.objects.filter(email=email_as_username)
        if not user.exists():
            raise forms.ValidationError("Username does not exists")
        return email_as_username

    def clean_password(self):
        user_exact_password = False
        passwords = self.cleaned_data['password']
        try:
            email_as_username = self.cleaned_data['email_as_username'].lower()
            print(email_as_username, 'email_as_username')
            user = UserBase.objects.get(email=email_as_username)
            print(user, "user")
            user_exact_password = user.check_password(passwords)
            print(user.check_password(passwords), ' | ', user_exact_password, ' | ', 'user_exact_password')
        except:
            pass
        if not user_exact_password:
            raise forms.ValidationError("Wrong password")
        return passwords

    """def clean_password(self):
        passwords = self.cleaned_data
        if UserBase.objects.filter(user=request.user).exists():
        if passwords['password'] != passwords['password2']:
            raise forms.ValidationError("Both passwords do not match")
        return passwords['password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken, please use another Email0")
        return email"""

class UserAddressForm(forms.ModelForm):
    full_name = forms.CharField(label='Fullname', min_length=2, max_length=100)
    phone = forms.CharField(label='Phone', min_length=7, max_length=25)
    email = forms.CharField(label='Town/City', min_length=2, max_length=250)
    postal_code = forms.CharField(label='Postal code', min_length=2, max_length=20)
    city = forms.CharField(label='Town/City', min_length=2, max_length=250)
    address_line = forms.CharField(label='Address', min_length=10, max_length=250)
    

    class Meta:
        model = Address
        fields = ["full_name", "phone", "email", "postal_code", "city", "address_line"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-input", "name": "full_name", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-input", "name": "phone", "placeholder": "Phone No"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-input", "name": "email", "placeholder": "Email"}
        )
        self.fields["postal_code"].widget.attrs.update(
            {"class": "form-input", "name": "postal_code", "placeholder": "Post Code"}
        )
        self.fields["city"].widget.attrs.update(
            {"class": "form-input", "name": "city", "placeholder": "Town or City"}
        )
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-input", "name": "address_line", "placeholder": "Address"}
        )


    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if full_name.isdigit():
            raise forms.ValidationError("Name cannot contain digits")
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
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
        if contain_unwanted_characterz:
            raise forms.ValidationError("Email contains unwanted character")

        # checks & executes if it doesnt contains characters at all / bad character
        elif not contain_unwanted_characterz:
            ends_with = re.search(r'@yahoo.com$|gmail.com$|hotmail.com$', email)
            if ends_with != None:
                pass
            else:
                raise forms.ValidationError("invalid email pattern, must end with [gmail.com, yahoo.com etc]")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("phone can contain only digits")
        return phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not postal_code.isdigit():
            raise forms.ValidationError("postal code can contain only digits")
        return postal_code


    