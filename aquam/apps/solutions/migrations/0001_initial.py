# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WaterUse',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('api', models.CharField(max_length=20)),
                ('frac_date', models.DateField()),
                ('state', models.CharField(max_length=20, null=True)),
                ('county', models.CharField(max_length=20, null=True)),
                ('well_name', models.CharField(max_length=50, null=True)),
                ('latitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('longtitude', models.DecimalField(max_digits=20, decimal_places=6)),
                ('horizontal_length', models.DecimalField(max_digits=20, decimal_places=3)),
                ('water_use', models.DecimalField(max_digits=20, decimal_places=3)),
            ],
        ),
    ]
