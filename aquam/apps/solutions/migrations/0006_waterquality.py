# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0005_producedwater'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterQuality',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('well_number', models.PositiveIntegerField()),
                ('tds', models.DecimalField(max_digits=20, decimal_places=3)),
                ('chloride', models.DecimalField(max_digits=20, decimal_places=3)),
                ('sodium', models.DecimalField(max_digits=20, decimal_places=3)),
                ('calcium', models.DecimalField(max_digits=20, decimal_places=3)),
                ('iron', models.DecimalField(max_digits=20, decimal_places=3)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
