from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    
    #This decides where the file should be saved inside your MEDIA_ROOT.
    return 'images/{filename}'.format(filename=filename)

class Posts(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(
        max_length=80, blank=False, null=False)
    description = models.TextField()
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)