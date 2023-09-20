from django.contrib import admin

from .models import OrderedItemDetail, OrderReciept, Checkout

admin.site.register(Checkout)
admin.site.register(OrderedItemDetail)
admin.site.register(OrderReciept)

