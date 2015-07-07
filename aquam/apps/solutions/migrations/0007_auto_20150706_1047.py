# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0006_waterquality'),
    ]

    operations = [
        migrations.RenameField(
            model_name='waterquality',
            old_name='well_number',
            new_name='wells_number',
        ),
    ]
