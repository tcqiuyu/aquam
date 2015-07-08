# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0008_auto_20150706_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterquality',
            name='volume',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=3),
        ),
    ]
