from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    name = models.CharField(max_length=256, default="New Photo Name")
    model_name = models.CharField(max_length=256, default="Camera Model Name")
    create_date = models.DateTimeField()
    upload_date = models.DateTimeField(auto_now_add=True)
