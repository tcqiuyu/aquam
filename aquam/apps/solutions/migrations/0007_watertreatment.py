# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0006_waterquality'),
    ]

    operations = [
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
                ('wqfrac_cf', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('wqfrac_sc', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('wqfrac_ro', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_cf', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_sc', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_ro', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_vrec_cf', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_vrec_sc', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
                ('vfresh_vrec_ro', models.DecimalField(null=True, max_digits=20, decimal_places=3)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
