# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='photos/')),
                ('name', models.CharField(max_length=256, default='New Photo Name')),
                ('model_name', models.CharField(max_length=256, default='Camera Model Name')),
                ('create_date', models.DateTimeField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.ImageField(upload_to='photos/')),
                ('md5sum', models.CharField(unique=True, max_length=36, default='')),
            ],
        ),
    ]
