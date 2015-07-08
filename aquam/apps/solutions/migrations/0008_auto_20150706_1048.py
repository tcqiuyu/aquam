# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0007_auto_20150706_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterquality',
            name='calcium',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='waterquality',
            name='chloride',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='waterquality',
            name='iron',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='waterquality',
            name='sodium',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='waterquality',
            name='tds',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=3),
        ),
    ]
