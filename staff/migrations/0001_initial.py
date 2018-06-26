# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-21 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('initialies', models.TextField(max_length=20)),
                ('email', models.TextField(blank=True, null=True)),
                ('loginname', models.CharField(max_length=255)),
                ('accessinvoice', models.BooleanField()),
                ('accessstatistics', models.BooleanField()),
            ],
            options={
                'db_table': 'staff',
                'ordering': ['pk'],
            },
        ),
    ]
