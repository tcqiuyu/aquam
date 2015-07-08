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
    ]
