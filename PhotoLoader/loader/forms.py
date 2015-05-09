from django import forms

class PhotoLoader(forms.Form):
    image_field = forms.ImageField(label="Upload your photo")
    name_field = forms.CharField(label="Photo title", max_length=256)