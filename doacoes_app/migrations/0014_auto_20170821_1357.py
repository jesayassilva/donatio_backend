# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes_app', '0013_auto_20170819_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doacao',
            name='foto',
            field=models.FileField(upload_to=''),
        ),
    ]