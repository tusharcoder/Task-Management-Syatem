# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-19 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='assets/media/image/face-2.jpg', upload_to='/static_files/assets/media/image/'),
        ),
    ]
