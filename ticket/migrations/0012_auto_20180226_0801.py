# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-26 08:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0011_auto_20180226_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 26, 8, 1, 25)),
        ),
    ]