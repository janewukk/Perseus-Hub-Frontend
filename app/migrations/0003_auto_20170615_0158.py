# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 01:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170615_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='dataset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Dataset'),
        ),
    ]
