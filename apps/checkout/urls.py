from django.urls import include, path
from django.conf.urls import url

from . import views

app_name = "checkout_"

urlpatterns = [
    path("delivery-choices", views.deliverychoices, name="delivery_choice"),
    path("cart_update_delivery/", views.cart_update_delivery, name="cart_update_delivery"),
    path("delivery_address/", views.delivery_address, name="delivery_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("complete-payment", views.complete_payment, name="complete_payment"),
    path("auth-check", views.user_details_authenticated, name="user_details_authenticated"),
]
