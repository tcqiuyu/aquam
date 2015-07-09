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
    ]
