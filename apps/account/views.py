import json

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core import serializers
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from apps.order.models import Address
from .forms import RegistrationForm, UserLoginForm, UserAddressForm
from .models import UserBase
from .token import account_activation_token

from apps.product.models import Product, Category
from apps.order.models import OrderReciept, Address



@csrf_exempt
def userLogin(request):
    message = {}
    status = 400
    if request.method == "POST":
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            user = authenticate(
                request,
                username = loginForm.cleaned_data['email_as_username'],
                password = loginForm.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message['key'] = "Successful"
                message['value'] = f"{user.user_name} has been logged in"
                status = 200
            else:
                message['key'] = "Failed"
                message['value'] = "Login Failed Because User Wasn't Authenticated"
        else:
            errors = loginForm.errors.as_data()
            err_field = list(errors.keys())
            message['key'] = err_field[0]
            message['value'] = str(errors[err_field[0]]).split("'")[1]
    else:
        pass
    print(status, "statusstatusstatus")
    response = JsonResponse({'msg': message}, status=status)
    return response

@csrf_exempt
def userLogout(request):
    if request.user.is_authenticated:
        logout(request)
    response = JsonResponse({})
    return response

def account_registration(request):
    message = {}
    status = 400
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        registrationform = RegistrationForm(request.POST)
        if registrationform.is_valid():
            user=registrationform.save(commit=False)
            user.email=registrationform.cleaned_data['email']
            user.user_name=registrationform.cleaned_data['user_name']
            user.set_password(registrationform.cleaned_data['password'])
            user.is_active=False
            user.save()
            user.is_active=False
            status = 200
        else:
            errors = registrationform.errors.as_data()
            err_field = list(errors.keys())
            message['key'] = err_field[0]
            message['value'] = str(errors[err_field[0]]).split("'")[1]
    else:
        pass
    response = JsonResponse({'msg': message}, status=status)
    return response

@login_required
@csrf_exempt
def add_address(request):
    message = {}
    status = 400
    data = {}
    if request.method == "POST":
        addressForm = UserAddressForm(request.POST)
        print(addressForm)
        if addressForm.is_valid():
            address=addressForm.save(commit=False)
            address.customer=request.user
            data['full_name'] = address.full_name=addressForm.cleaned_data['full_name']
            data['email'] = address.email=addressForm.cleaned_data['email']
            data['phone'] = address.phone=addressForm.cleaned_data['phone']
            data['postal_code'] = address.post_code=addressForm.cleaned_data['postal_code']
            data['city'] = address.city=addressForm.cleaned_data['city']
            data['address_line'] = address.address_line=addressForm.cleaned_data['address_line']
            address.save()
            data['pk'] = address.id
            status = 200
        else:
            errors = addressForm.errors.as_data()
            err_field = list(errors.keys())
            message['key'] = err_field[0]
            message['value'] = str(errors[err_field[0]]).split("'")[1]
    else:
        pass
    print(message, status, "statusstatusstatus")
    response = JsonResponse({'msg': message, "data": data}, status=status)
    return response

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("cart_:cart_details"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserEditAddressForm(instance=address)
    return render(request, "account/user/edit_address.html", {"form": address_form})


@login_required
def set_default(request):
    if request.POST.get('action') == 'post':
        address_id = request.POST.get('address_id')
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        Address.objects.filter(id=address_id, customer=request.user).update(default=True)

    response = JsonResponse({'address_id':address_id})
    return response

@login_required
def user_orders(request):
    user_id = request.user.id
    orders = OrderReciept.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

