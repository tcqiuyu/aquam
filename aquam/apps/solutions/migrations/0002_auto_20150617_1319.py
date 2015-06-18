# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wateruse',
            options={'ordering': ['api']},
        ),
        migrations.AlterModelTable(
            name='wateruse',
            table='wateruse_demo',
        ),
    ]
