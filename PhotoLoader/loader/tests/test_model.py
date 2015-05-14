from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from .factory import PhotoFactory

class ModelTest(TestCase):
    def setUp(self):
        self.photo = PhotoFactory()

    def tearDown(self):
        self.photo.delete()

    def test_save(self):
        self.assertTrue(self.photo.md5sum)
        # prepare new upload image
        thumb = Image.new('RGB', (1024, 768), 'red')  # the same size and color as self.photo.image
        thumb_io = BytesIO()
        thumb.save(thumb_io, format='JPEG')

        # prevent the purposefully-thrown exception from breaking the entire unittest's transaction
        with transaction.atomic():
            self.assertRaisesMessage(IntegrityError, "UNIQUE constraint failed: loader_photo.md5sum",
                                     PhotoFactory, image = ContentFile(thumb_io.getvalue(), "test.jpg"),
                                     name = "Uploaded Photo 1")

        # no problems with the new different image
        up_photo = PhotoFactory(name = "Uploaded Photo 1")  # new blue image
        self.assertNotEqual(up_photo.md5sum, self.photo.md5sum)


