from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from PIL import Image

from .factory import PhotoFactory

class ModelTest(TestCase):
    def setUp(self):
        self.photo = PhotoFactory()
        self.up_photo = None

    def tearDown(self):
        # delete created files from media/photos folder
        self.photo.delete()
        self.up_photo.delete()

    def test_save(self):
        self.assertTrue(self.photo.md5sum)
        # prepare new upload image
        thumb = Image.new('RGB', (1024, 768), 'red')  # the same size and color
                                                      # as self.photo.image
        thumb_io = BytesIO()
        thumb.save(thumb_io, format='JPEG')

        # prevent the purposefully-thrown exception from breaking the entire
        # unittest's transaction
        with transaction.atomic():
            self.assertRaisesMessage(IntegrityError, "UNIQUE constraint failed: "
                                                     "loader_photo.md5sum",
                                     PhotoFactory,
                                     image = ContentFile(thumb_io.getvalue(),
                                                         "test.jpg"),
                                     name = "Uploaded Photo 1",
                                     thumbnail = None  # we won't generate
                                                       # thumbnail image
                                     )
        path = default_storage.path(name="photos/test.jpg")
        default_storage.delete(path)  # remove photo created in 'media' folder

        # no problems with the new different image
        self.up_photo = PhotoFactory(name = "Uploaded Photo 1")  # new blue image
        self.assertNotEqual(self.up_photo.md5sum, self.photo.md5sum)


