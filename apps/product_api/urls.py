from django.urls import path
from . import views




app_name="product_api_"
urlpatterns = [
    path("all-product", views.all_product, name="all_product"),
    path("single-product/<slug:str>/<int:id>", views.single_product, name="single_product"),
    path("all-vendor-product", views.all_vendor_product, name="all_vendor_product"),
    path("best-selling-product", views.best_selling_product, name="best_selling_product"),
    path("all-category", views.all_category, name="all_category"),
    
]

