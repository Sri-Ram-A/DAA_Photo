from . import views
from django.urls import path
from .views import ImageUploadView

urlpatterns = [
    path("",views.HelloWorld.as_view()),
    path('images/', ImageUploadView.as_view(), name='image-upload'),
]
