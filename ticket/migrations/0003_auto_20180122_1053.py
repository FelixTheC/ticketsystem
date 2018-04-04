# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-22 10:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20180122_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2018, 1, 22, 10, 53, 9, 567523, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='from_email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
