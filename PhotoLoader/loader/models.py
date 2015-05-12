import hashlib
from django.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    name = models.CharField(max_length=256, default="New Photo Name")
    model_name = models.CharField(max_length=256, default="Camera Model Name")
    create_date = models.DateTimeField()
    upload_date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='photos/')
    md5sum = models.CharField(unique=True, max_length=36, default='')

    def save(self, *args, **kwargs):
        if not self.pk:
            md5 = hashlib.md5()
            for chunk in self.image.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super(Photo, self).save(*args, **kwargs)
