from datetime import datetime, timedelta
from django import forms
from PIL import Image

class PhotoLoader(forms.Form):
    image_field = forms.ImageField(label="Upload your photo")
    name_field = forms.CharField(label="Photo title", max_length=256)

    def clean_image_field(self):
        data = self.cleaned_data['image_field']
        img = Image.open(data)
        try:
            exif = img._getexif()
        except AttributeError:
            raise forms.ValidationError("Uploaded image has no EXIF data!",
                                        code='invalid')
        if not exif: exif = {}  # set empty dictionary if we didn't find any
                                # exif data to prevent 'get' error
        created_date = exif.get(0x9003)  # get "DateTimeOriginal" EXIF tag
        now = datetime.now()
        if created_date:
            created_date_dt = datetime.strptime(created_date,
                                                "%Y:%m:%d %H:%M:%S")
            # we won't bother about leap-year
            if (now - timedelta(days=365)) > created_date_dt:
                raise forms.ValidationError("Uploaded image older than one "
                                            "year!", code='invalid')
        else:
            raise forms.ValidationError("There is no \"DateTimeOriginal\" tag "
                                        "in EXIF data!", code='invalid')
        return data