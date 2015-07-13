# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeoWaterUse',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('api', models.CharField(max_length=20)),
                ('well_name', models.CharField(max_length=100, null=True)),
                ('frac_date', models.DateField()),
                ('state', models.CharField(max_length=20, null=True)),
                ('county', models.CharField(max_length=20, null=True)),
                ('latitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('longitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('horizontal_length', models.DecimalField(max_digits=20, decimal_places=3)),
                ('water_use', models.DecimalField(max_digits=20, decimal_places=3)),
            ],
            options={
                'ordering': ['api'],
            },
        ),
    ]
