from datetime import datetime
from io import BytesIO
import os

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_GET
from django.views.generic import DeleteView

from PIL import Image
from PIL.ExifTags import TAGS

from .forms import PhotoLoader
from .models import Photo


def _get_exif_dict(file):
    """
    Returns dictionary with extracted
    from uploaded photo exif information.

    :param file: File object to extract exif from.
    :return: dict
    """
    file = Image.open(file)
    exif_dict = {}
    exif = file._getexif()
    if exif:
        for (k, v) in exif.items():
            exif_dict.update({TAGS.get(k): v})
        return exif_dict
    return None


def _create_thumbnail(image):
    """
    Returns new file of thumbnail image.

    :param image: Image file to create thumbnail from
    :return: InMemoryUploadedFile
    """
    with Image.open(image) as img:
        thumb = img.copy()  # copy file to prevent original image modification with the thumbnail function
        thumb.thumbnail((128, 128), Image.NEAREST)
        thumbnailBytes = BytesIO()
        thumb.save(thumbnailBytes, 'JPEG')
        newFile = InMemoryUploadedFile(thumbnailBytes, None, 'thumb_%s.jpg' % image.name[:image.name.find(".")],
                                       'image/jpeg', len(thumbnailBytes.getvalue()), None)
        return newFile


@require_http_methods(['GET', 'POST'])
def upload_file(request):
    args = {}
    if request.method == 'POST':
        form = PhotoLoader(request.POST, request.FILES)
        if form.is_valid():
            # img_file = request.FILES['image_field']
            img_file = form.cleaned_data['image_field']
            exif_dict = _get_exif_dict(img_file)
            thumbnail = _create_thumbnail(img_file)
            newphoto = Photo(
                image = img_file,
                name = form.cleaned_data['name_field'],
                model_name = "%s %s" % (exif_dict['Make'], exif_dict['Model']),
                create_date = datetime.strptime(exif_dict["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S"),
                thumbnail = thumbnail,
            )
            try:
                newphoto.save()
                return HttpResponseRedirect('/table/')
            except IntegrityError:
                # delete currently uploaded files from MEDIA_ROOT
                for path in (newphoto.image.path, newphoto.thumbnail.path):
                    os.remove(path)
                form.add_error(None, "Current image is already uploaded!")

    else:
        form = PhotoLoader()

    args['form'] = form
    return render(request, "loader/index.html", args)

@require_GET
def table(request):
    photos = Photo.objects.all()
    return render(request, "loader/photos.html", {'photos': photos})

class DeletePhoto(DeleteView):
    """
    Generic class for delete link.
    """
    model = Photo
    success_url = reverse_lazy('table')
    template_name = 'loader/delete_photo.html'