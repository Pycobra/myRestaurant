from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core import serializers

from apps.order.models import OrderReciept, OrderedItemDetail, Address, Checkout
from apps.cart.cart import Cart

from .models import DeliveryOptions, PaymentSelections


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
@csrf_exempt
def cart_update_delivery(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = cart.cart_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {"delivery_id": delivery_type.id}
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True
        response = JsonResponse({"delivery_price": delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if addresses:
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].pk)}
        else:
            session["address"]["address_id"] = str(addresses[0].pk)
            session.modified = True
        return render(request, "order/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):
    # print(request.COOKIES)
    session = request.session
    if "address" not in session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        id = session["address"]['address_id']
        address = Address.objects.get(id=id)

    return render(request, "checkout/payment_selection.html", {'address': address})


@login_required
@csrf_exempt
def complete_payment(request):
    session = request.session
    cart = Cart(request)
    if request.POST:
        action= request.POST.get('action')
        if action == "flutterwave-payment":
            ref = request.POST.get('tx_ref')
        elif action == "paystack-payment":
            ref = request.POST.get('ref')
        # amount = request.POST.get('amount')
        total_paid = request.POST.get('total_paid')
        payment_id = session["payment"]["payment_id"]
        address_id = session["address"]["address_id"]
        delivery_id = session["purchase"]["delivery_id"]
        address = request.user.user_address.get(id=address_id)
        payment_selection = PaymentSelections.objects.get(id=payment_id)
        delivery_instructions = DeliveryOptions.objects.get(id=delivery_id)
        order = OrderReciept.objects.create(
            user_id=request.user.id, 
            delivery_address=address, 
            delivery_instructions=delivery_instructions,
            total_paid=total_paid, 
            payment_option=payment_selection,
            total_quantity= cart.__len__()
        )
        for item in cart:
            OrderedItemDetail.objects.create(
                order=order, product=item['product'],
                amount=item['total_price'], 
                quantity=item['quantity']
            )
        verified = order.verify_payment(total_paid, ref, action)
        if verified:
            order.verified = True
            order.save()
            Checkout.objects.create(order=order, ref=ref)
            messages.success(request, "Payment verification was sucessfull")
        else:
            messages.success(request, "Your payment verification failed")
    response = JsonResponse({})
    return response


@csrf_exempt
def user_details_authenticated(request):
    session = request.session
    cart = Cart(request)
    mydeliveryopt = {}
    mydeliveryadd = {}
    if request.GET:
        payment_id = request.GET.get('paymentID')
        if "payment" not in session:
            session["payment"] = {"payment_id": payment_id}
        else:
            session["payment"]["payment_id"] = payment_id
            session.modified = True
        
        if request.GET.get('action') == 'paystack-payment':
            key = settings.PAYSTACK_PUBLIC_KEY
        if request.GET.get('action') == 'flutterwave-payment':
            key = settings.FLUTTERWAVE_PUBLIC_KEY
        if "purchase" in request.session:
            delivery_id = session["purchase"]["delivery_id"]
            mydeliveryopt = DeliveryOptions.objects.filter(id=delivery_id)
        if "address" in request.session:
            address_id = session["address"]["address_id"]
            mydeliveryadd = Address.objects.filter(id=address_id)
    serialized_delivery = serializers.serialize('python', mydeliveryopt)
    serialized_address = serializers.serialize('python', mydeliveryadd)
    item = {}
    item['address'] = serialized_address
    item['delivery'] = serialized_delivery
    if mydeliveryopt:
        userHasdeliveryopt = True
    else:   
        userHasdeliveryopt = False
    if mydeliveryadd:
        userHasdeliveryadd = True
    else:
        userHasdeliveryadd = False
    response = JsonResponse({
        "userHasdeliveryopt": userHasdeliveryopt, 
        "userHasdeliveryadd": userHasdeliveryadd, 
        'amt': cart.get_total_cost(), 
        "item":item,
        # "email": mydeliveryadd.email, 
        # "delivery_price": mydeliveryopt.delivery_price,
        # "phone": mydeliveryadd.phone,
        'key': key,
        'user_name': request.user.user_name,

    })
    return response


        







































