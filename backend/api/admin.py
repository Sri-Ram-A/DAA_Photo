from django.contrib import admin
from . import models
# Register your models here.
# admin.site.register(models.Posts)

@admin.register(models.Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'uploaded_at') #allows you to see a tabular format
