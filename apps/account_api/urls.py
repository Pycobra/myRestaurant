from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views




app_name="account_api_"
urlpatterns = [
    path('token/obtain-token/', views.TokenObtainPairViewWithUserObject.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    
    path("create-address", views.create_address, name="create-address"),
    path("create-account", views.create_account, name="create_account"),
    path('logout/blacklist/', views.BlacklistTokenLogoutView.as_view(), name ='api-logout'),  
    path("user-address/<slug:id>/", views.user_address, name="user-address"),  
]

