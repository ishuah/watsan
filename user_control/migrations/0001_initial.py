# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 09:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next', models.CharField(default=b'/', max_length=100)),
                ('number', models.CharField(blank=True, max_length=20)),
                ('secondary_number', models.CharField(blank=True, max_length=20)),
                ('gender', models.CharField(blank=True, choices=[(b'male', b'Male'), (b'female', b'Female')], max_length=10)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=b'UserAvatars')),
                ('has_mpesa', models.NullBooleanField()),
                ('organization', models.CharField(blank=True, max_length=255)),
                ('confirmation_code', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_control_userprofile',
            },
        ),
    ]
