# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 16:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes_app', '0006_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='user',
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]
