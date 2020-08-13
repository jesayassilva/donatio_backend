# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 15:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes_app', '0004_doacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='doacao',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
