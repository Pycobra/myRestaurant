from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import login, logout

from apps.product.models import Product, Category
from apps.checkout.models import PaymentSelections
from apps.account.forms import UserLoginForm, RegistrationForm, UserAddressForm

from apps.checkout.models import DeliveryOptions
from apps.order.models import Address  
from apps.vendor.models import Vendor    



def frontpage(request):
    session = request.session
    mydeliveryopt = {}
    mydeliveryadd = {}
    deliveryoptions = {}
    addressoptions = {}
    myPaymentOpt = {}
    if "purchase" in request.session:
        delivery_id = session["purchase"]['delivery_id']
        mydeliveryopt = DeliveryOptions.objects.get(id=delivery_id)
        deliveryoptions = DeliveryOptions.objects.filter(is_active=True).exclude(id=delivery_id)
    if "address" in request.session:
        address_id = session["address"]['address_id']
        mydeliveryadd = Address.objects.get(id=address_id)
        addressoptions = Address.objects.all().exclude(id=address_id)
    if "payment" in request.session:
        payment_id = session["payment"]['payment_id']
        myPaymentOpt = PaymentSelections.objects.get(id=payment_id)
    paymentOptions = PaymentSelections.objects.all()
    #all_products = Product.objects.prefetch_related("product_images").filter(is_active=True, in_stock=True).order_by('-created_at')
    all_products = Product.objects.filter(is_active=True, in_stock=True).order_by('-created_at')
    # categories = Category.objects.filter(level=0)
    cat_list = []
    for i in all_products:
        cat_list.append(i.category)
    categories = list(set(cat_list))

    vendor_categories = Category.objects.filter(level=0)
    all_vendor = Vendor.objects.all()
    return render(request, 'core/frontpage.html', {'all_products': all_products, 'categories':categories, 
                                                    'loginForm':UserLoginForm, 'registerform':RegistrationForm,
                                                   'addressForm':UserAddressForm, 'mydeliveryopt':mydeliveryopt, 'mydeliveryadd':mydeliveryadd,
                                                   'deliveryoptions':deliveryoptions,"addressoptions":addressoptions,
                                                   'images': ['food-cover1','food-cover2','food-cover3','food-cover4'], 
                                                   'vendor_categories':vendor_categories, 'all_vendor':all_vendor, 
                                                   'myPaymentOpt': myPaymentOpt, 'paymentOptions': paymentOptions,
                                                    # 'vendor_product': product
                                                    })