import hashlib
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models

class PhotoFilesStorage(FileSystemStorage):
    """
    Custom storage class. Has overridden method _save for avoiding duplicate files saving.
    """
    def get_available_name(self, name, max_length=None):
        """
        Save the name of uploaded file the same.
        """
        return name

    def _save(self, name, content):
        """
        Check if file exists in storage. Avoid default save if it does.
        """
        if self.exists(name):
            raise ValidationError("Uploaded file already exists!", code='invalid')

        return super(PhotoFilesStorage, self)._save(name, content)

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/', storage=PhotoFilesStorage())
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
