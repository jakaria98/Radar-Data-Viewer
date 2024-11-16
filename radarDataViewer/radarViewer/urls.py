from django.urls import path
from .views import upload_and_process_file

urlpatterns = [
    path('api/upload/', upload_and_process_file, name='upload_sort_file'),
]
