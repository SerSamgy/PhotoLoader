from datetime import datetime
from itertools import cycle

from django.core.files.base import ContentFile

import factory
import factory.django
import factory.fuzzy

from ..models import Photo

_colors = cycle(('red', 'blue', 'yellow', 'green', 'black'))

class PhotoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Photo
        factory.django_get_or_create = ('image', 'thumbnail', 'md5sum',)

    @factory.lazy_attribute_sequence
    def image(self, n):
        return ContentFile(
            factory.django.ImageField()._make_data({'width': 1024, 'height': 768,
                                                    'color': _colors.__next__()}
            ), "example_%d.jpg" % n
        )

    name = "Default Photo Name"
    model_name = "Canon EOS 5D"
    create_date = factory.fuzzy.FuzzyNaiveDateTime(datetime(2014, 5, 20,
                                                            19, 40, 30))
    upload_date = factory.fuzzy.FuzzyNaiveDateTime(datetime(2015, 4, 10,
                                                            10, 15, 38))

    @factory.lazy_attribute_sequence
    def thumbnail(self, n):
        return ContentFile(
            factory.django.ImageField()._make_data({'width': 128, 'height': 128}
            ), "thumb_example_%d.jpg" % n
        )

    md5sum = ""