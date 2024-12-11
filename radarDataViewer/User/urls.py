from django.urls import path
from .views import *

urlpatterns = [
    path('api/login/', login),
    path('api/register/', register),
    path('api/update/', update_user),
    path('api/test_token/', test_token),
]
