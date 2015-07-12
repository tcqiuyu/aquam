# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProducedWater',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('days', models.PositiveIntegerField()),
                ('well_1', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_2', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_3', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_4', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_5', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_6', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
                ('well_7', models.DecimalField(null=True, max_digits=20, decimal_places=0)),
            ],
            options={
                'ordering': ['days'],
            },
        ),
        migrations.CreateModel(
            name='WaterQuality',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('wells_number', models.PositiveIntegerField()),
                ('tds', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('chloride', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('sodium', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('calcium', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('iron', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('volume', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WaterTreatment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=50)),
                ('days', models.PositiveIntegerField()),
                ('stages', models.PositiveIntegerField()),
                ('constituent', models.CharField(max_length=20)),
                ('quality', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfrac', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('wqfrac_iter_1', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_iter_1', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('ratio_iter_1', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('wqfrac_iter_2', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_iter_2', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('ratio_iter_2', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('wqfrac_iter_3', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_iter_3', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('ratio_iter_3', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WaterUse',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('api', models.CharField(max_length=20)),
                ('frac_date', models.DateField()),
                ('state', models.CharField(max_length=20, null=True)),
                ('county', models.CharField(max_length=20, null=True)),
                ('well_name', models.CharField(max_length=100, null=True)),
                ('latitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('longtitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('horizontal_length', models.DecimalField(max_digits=20, decimal_places=3)),
                ('water_use', models.DecimalField(max_digits=20, decimal_places=3)),
            ],
            options={
                'ordering': ['api'],
            },
        ),
    ]
