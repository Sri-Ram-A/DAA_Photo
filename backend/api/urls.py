from . import views
from django.urls import path

urlpatterns = [
    path("",views.HelloWorld.as_view()),
    path('images/', views.CreatePost.as_view(), name='post-list'),
    path('images/<int:pk>/', views.CreatePost.as_view(), name='post-detail'),
]
