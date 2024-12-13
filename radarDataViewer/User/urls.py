from django.urls import path
from . import views

from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('api/login/', views.login_view, name='login'),
    path('api/register/', views.register, name='register'),
    path('api/token/', auth_views.obtain_auth_token, name='obtain_auth_token'),  # DRF token endpoint
    path('api/update/', views.update_user, name='update_user'),
    path('api/allusers/', views.get_all_users, name='get_all_user'),
]
