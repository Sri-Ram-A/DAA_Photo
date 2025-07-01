from . import views
from django.urls import path

urlpatterns = [
    path("",views.HelloWorld.as_view()),
    path("images/",views.CreatePost.as_view(),name="create_post"),
    path("clear/", views.ClearAllData.as_view(), name="clear_all_data"),

]
