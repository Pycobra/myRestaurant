from django.contrib import admin

from .models import UserBase, Address


@admin.register(UserBase)
class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Address)
