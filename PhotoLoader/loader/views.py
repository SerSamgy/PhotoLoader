from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from PIL import Image
from PIL.ExifTags import TAGS

from PhotoLoader.loader.forms import PhotoLoader
from PhotoLoader.loader.models import Photo

def upload_file(request):
    if request.method == 'POST':
        form = PhotoLoader(request.POST, request.FILES)
        if form.is_valid():
            file = Image.open(request.FILES['image_field'])
            exif_dict = {}
            for (k,v) in file._getexif().items():
                exif_dict.update({TAGS.get(k): v})

            newphoto = Photo(
                image = request.FILES['image_field'],
                name = form.cleaned_data['name_field'],
                model_name = "%s %s" % (exif_dict['Make'], exif_dict['Model']),
                create_date = datetime.strptime(exif_dict["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S"),
            )
            newphoto.save()
            return HttpResponseRedirect('/table/')
    else:
        form = PhotoLoader()
    return render(request, "loader/index.html", {'form': form})

def table():
    return None