from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login),
    path('api/register/', views.register),
    path('api/update/', views.update_user),
   # path('api/test_token/', views.test_token),
]
