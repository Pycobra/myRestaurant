from decimal  import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.forms import inlineformset_factory, modelformset_factory
from django.db.models import Q
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site

from apps.account.models import UserBase
from apps.product.models import Product, Category
from apps.cart.cart import Cart
from .models import Vendor



def select_category(request):
    if request.GET:
        vendor_id = request.GET.get('vendorID')
        category_id = request.GET.get('categoryID')
        if request.GET.get('action') == 'all-vendor-products':
            product_array = Product.objects.filter(vendor__id=vendor_id)
        
        else:
            product_array = Product.objects.filter(vendor__id=vendor_id).filter(category__id=category_id)
        serialized_queryset = serializers.serialize('python', product_array)
        product = {}
        product['table'] = serialized_queryset
        response = JsonResponse({'product': product})
        return response




    
    
