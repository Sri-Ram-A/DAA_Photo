from django.contrib import admin
from django.urls import path,include
from minio_handler import views

urlpatterns = [
    path('upload/',views.upload_files),
    path('list/',views.list_files),
     path('download/<str:filename>/', views.download_file, name='download_file'),

]