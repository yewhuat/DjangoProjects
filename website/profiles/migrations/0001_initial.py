# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 11:43
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
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('mobileno', models.CharField(max_length=15)),
                ('category', models.IntegerField(default=0)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nric', models.CharField(max_length=14)),
                ('birth_date', models.DateField(default='1900-01-01')),
                ('address01', models.CharField(max_length=255)),
                ('address02', models.CharField(max_length=255)),
                ('address03', models.CharField(max_length=255)),
                ('state', models.CharField(default='Kuala Lumpur', max_length=20)),
                ('postcode', models.CharField(default='50000', max_length=10)),
                ('country', models.CharField(default='Malaysia', max_length=255)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
