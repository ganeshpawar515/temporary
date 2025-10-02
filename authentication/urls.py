from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CustomTokenObtainPairView,logged_in_user

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logged/",logged_in_user,name="logged_in_user"),
    # path("users/",UserReadView.as_view())  
]
