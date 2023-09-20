from django.urls import path
from . import views




app_name="vendor_api_"
urlpatterns = [
    path("all-vendor", views.all_vendor, name="all_vendor"),
    path("single-vendor/<slug:id>", views.single_vendor, name="single_vendor"),
    path("recent-added-vendor", views.recent_added_vendor, name="recent_added_vendor"),
    path("best-selling-vendor", views.best_selling_vendor, name="best_selling_vendor"),
]

