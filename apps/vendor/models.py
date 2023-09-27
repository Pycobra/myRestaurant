#from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.account.models import UserBase
import datetime
import secrets



class Vendor(models.Model):
    store_name = models.CharField(max_length=255, unique=True)
    unique_id =  models.CharField(max_length=50, unique=True)
    vendor_image = models.ImageField(verbose_name=_("profile image"),
                                   help_text=_("Upload a your image"),
                                   upload_to="images/uploads/vendor/",
                                   default="images/shop.png")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(UserBase, related_name="which_vendor", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'List of Vendors'
        ordering=['store_name']

    def save(self, *args, **kwargs) -> None:
        while not self.unique_id:
            unique_id = secrets.token_urlsafe(33)
            object_with_similar_order_key = Vendor.objects.filter(unique_id=unique_id).exists()
            if not object_with_similar_order_key:
                self.unique_id = unique_id
        super().save(*args, **kwargs)

    #dunder
    #to make this the models name at admin area || and how to reference this model

    def __str__(self):
        return self.store_name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.price * item.quantity) for item in items)
        verbose_name_plural = 'List of Vendors'
