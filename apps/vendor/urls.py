from django.urls import path
from django.conf.urls import url

from . import views

app_name="vendor_"
urlpatterns = [
    path('select-category/', views.select_category, name="select_category"),
]
