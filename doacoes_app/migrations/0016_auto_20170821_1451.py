# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 14:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes_app', '0015_auto_20170821_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doacao',
            name='doador',
        ),
        migrations.RemoveField(
            model_name='doacao',
            name='produto',
        ),
        migrations.AlterField(
            model_name='doacao',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
