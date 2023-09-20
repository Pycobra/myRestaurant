import uuid
import secrets

from django.db import models
from django.core.files import File
from django.utils.translation import gettext_lazy as _


from apps.account.models import UserBase, Address
from apps.product.models import Product
from apps.checkout.models import PaymentSelections, DeliveryOptions
from apps.checkout.paystack import Paystack
from apps.checkout.flutterwave import FlutterWave




class OrderReciept(models.Model):
    """on_delete=models.CASCADE a user data shld remain despite delete since even
    a non signed up user can make an order"""
    user = models.ForeignKey(UserBase, blank=True, on_delete=models.CASCADE, related_name="order_user") # video used orders
    delivery_address = models.ForeignKey(
        Address, related_name="user_address_info", verbose_name=_(
            "address info"), null=True, on_delete=models.CASCADE
    )
    delivery_instructions = models.ForeignKey(
        DeliveryOptions, related_name="user_delivery_info", verbose_name=_(
            "delivery instructions"), null=True, on_delete=models.CASCADE
    )
    total_paid = models.DecimalField(max_digits=8, decimal_places=2)
    total_quantity = models.CharField(max_length=250, null=True)
    order_key = models.CharField(max_length=100, null=True)
    payment_option = models.ForeignKey(PaymentSelections, on_delete=models.CASCADE, related_name='customer_pay_option')
    verified = models.BooleanField(default=False)
    billing_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    class Meta:
        verbose_name_plural = 'Order Reciept'
        ordering = ['-created']

    # dunder
    # to make this the models name at admin area || and how to reference this model
    def __str__(self):
        return f"{self.order_key}"

    def save(self, *args, **kwargs) -> None:
        while not self.order_key:
            order_key = secrets.token_urlsafe(50)
            object_with_similar_order_key = OrderReciept.objects.filter(order_key=order_key).exists()
            if not object_with_similar_order_key:
                self.order_key = order_key
        super().save(*args, **kwargs)

    def verify_payment(self, amount, ref, action):
        paystack = Paystack()
        flutterwave = FlutterWave()
        if action == "paystack-payment":
            status, result = paystack.verify_payment(ref)
        elif action == "flutterwave-payment":
            status, result = flutterwave.verify_payment(ref)
        if status:
            product_amount=int(amount)
            payment_amount = int(result['amount'])
            if payment_amount / 100 == product_amount:
                return True
        return False



class OrderedItemDetail(models.Model):
    order = models.ForeignKey(OrderReciept,  related_name="order_items", on_delete=models.CASCADE)# video used items
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)# video used items
    amount = models.PositiveIntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        verbose_name_plural = 'Ordered Item Details'
        ordering = ['-order']

    # dunder
    # to make this the models name at admin area || and how to reference this model
    def __str__(self):
        return f"{self.product.title} has this order-key: {self.order.order_key}"

    """def get_total_price(self) -> int:
        amt = self.price * self.quantity
        return amt * 100"""



class Checkout(models.Model):
    order = models.ForeignKey(OrderReciept, related_name="checkout_order", on_delete=models.CASCADE)
    ref = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Checkout'
        ordering = ['-created']

    def __str__(self):
        return '%s' % self.ref
