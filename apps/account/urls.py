from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import UserLoginForm
from apps.core.views import frontpage



app_name="account_"
urlpatterns = [
    path('delete_confirmation/', auth_views.TemplateView.as_view(
        template_name='account/user/delete_confirmation.html'), name="delete_confirmation"),
    path('register/', views.account_registration, name="register"),
    path('login/', views.userLogin, name="login"),
    path('logout/', views.userLogout, name="logout"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/set_default/", views.set_default, name="set_default"),
]
