from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from . import views




app_name="checkout_api_"
urlpatterns = [
    path('delivery-options', views.delivery_options, name ='delivery-options'),
    path('payment-selections', views.payment_selections, name ='payment-selections'),
    path('complete-payment', views.complete_payment, name ='complete_payment'),
    path('paystack-public-key', views.paystack_public_key, name ='paystack_public_key'),
    ]

