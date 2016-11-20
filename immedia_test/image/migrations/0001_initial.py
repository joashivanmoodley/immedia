# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(null=True, blank=True)),
                ('image', models.URLField(max_length=250)),
                ('image_type', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('owner', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LandMark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('latitude', models.CharField(max_length=50, null=True, blank=True)),
                ('longitude', models.CharField(max_length=50, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('cc', models.CharField(max_length=5, db_index=True)),
                ('country', models.CharField(db_index=True, max_length=50, blank=True)),
                ('province', models.CharField(max_length=50, db_index=True)),
                ('region', models.CharField(max_length=50, db_index=True)),
                ('latitude', models.CharField(max_length=50, null=True, blank=True)),
                ('longitude', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('country', 'province', 'region')]),
        ),
        migrations.AddField(
            model_name='landmark',
            name='location',
            field=models.ForeignKey(blank=True, to='image.Location', null=True),
        ),
        migrations.AddField(
            model_name='image',
            name='land_mark',
            field=models.ForeignKey(blank=True, to='image.LandMark', null=True),
        ),
    ]
