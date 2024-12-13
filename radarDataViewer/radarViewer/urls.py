from django.urls import path
from . import views

urlpatterns = [
    path('api/upload/', views.upload_and_process_file, name='upload_sort_file'),
    path('api/files/', views.get_user_files, name='get_user_files'),
    path('api/files/<int:file_id>/', views.get_user_file, name='get_user_file'),
    path('api/files/<int:file_id>/delete/', views.delete_user_file, name='delete_user_file'),
]
