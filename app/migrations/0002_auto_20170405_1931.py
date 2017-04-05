# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 19:31
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='dataset',
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='bookmark',
            name='associated_property',
        ),
        migrations.AddField(
            model_name='dataset',
            name='analyzed_json_filename',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='dataset',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataset',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='publicized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dataset',
            name='raw_data',
            field=models.FileField(default='', upload_to='uploads/datasets/'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='title',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='dataset',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.DeleteModel(
            name='Property',
        ),
    ]
