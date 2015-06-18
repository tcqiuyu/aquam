# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0002_auto_20150617_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wateruse',
            name='well_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
