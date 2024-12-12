from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login_view, name='login'),
    path('api/register/', views.register, name='register'),
    path('api/update/', views.update_user, name='update'),
]
