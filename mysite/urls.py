from django.contrib import admin
from django.urls import path
from mysite.views import upload_files, list_files, download_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_files, name='upload_files'),    # Upload form
    path('', list_files, name='list_files'),                # List files on home page
    path('download/<str:filename>/', download_file, name='download_file'),
]
