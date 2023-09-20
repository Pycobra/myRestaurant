from django.urls import reverse
from django.template.context_processors import request
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify


from apps.vendor.models import Vendor
# from apps.account.models import UserBase






class Category(MPTTModel):
    """
    Category Table implementated with MPTT
    """
    name = models.CharField( verbose_name=_("Category Name"), help_text=_("Required and unique"), max_length=255)
    slug = models.SlugField(verbose_name=_("Category safe url"), max_length=255)
    parent = TreeForeignKey("self", related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]
    class Meta:
        """enforcing that there can not be two categories under a parent with same slug
        unique_together = ('slug', 'parent',)"""
        verbose_name =_("Category")
        verbose_name_plural = _("Categories")
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs


    def get_absolute_url(self):
        return reverse('product_:category_list', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.RESTRICT)
    vendor = models.ForeignKey(Vendor, related_name='vendors_products', on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    images = models.ImageField(verbose_name=_("image"), help_text=_("Upload a product image"),
                               upload_to="images/uploads/store", default="images/site_images/food-dummy.jpg")
    ingredient = models.TextField(verbose_name=_("ingredient"), help_text=_("Not Required"), blank=True)
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    price = models.IntegerField(verbose_name=_("Regular price"), help_text=_("Maximum 999.99"),
                                error_messages={
                                    "name": {"max_length": _("The price must be between 0 and 999.99.")},
                                })
    in_stock = models.BooleanField(verbose_name=_("Product availability"), help_text=_("Change product availability"), default=True)
    is_active = models.BooleanField(verbose_name=_("Product visibility"), help_text=_("Change product visibility"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name =_("Product")
        verbose_name_plural = _("Products")
    def __str__(self):
        return self.title



