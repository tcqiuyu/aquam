# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0004_auto_20150628_2123'),
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
    ]
