# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NobleWells',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('township', models.CharField(max_length=10, null=True)),
                ('range', models.CharField(max_length=10, null=True)),
                ('section', models.IntegerField(null=True)),
                ('idp', models.CharField(max_length=20, null=True)),
                ('area', models.CharField(max_length=10, null=True)),
                ('api', models.CharField(max_length=20, null=True)),
                ('latitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('longtitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('reservoir', models.CharField(max_length=20, null=True)),
                ('well_trajectory', models.CharField(max_length=20, null=True)),
                ('stages', models.IntegerField(null=True)),
                ('frac_fluid', models.CharField(max_length=20, null=True)),
                ('frac_date', models.DateField()),
                ('water_use', models.DecimalField(max_digits=20, decimal_places=1)),
            ],
        ),
        migrations.CreateModel(
            name='ProducedWater',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('well_1', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_2', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_3', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_4', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_5', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_6', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_7', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
            ],
        ),
        migrations.CreateModel(
            name='WaterQuality',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('wells_number', models.IntegerField()),
                ('volume', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('tds', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('sodium', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('chloride', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('calcium', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('iron', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
            ],
        ),
    ]
