# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stranke4', '0004_auto_20150304_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obisk',
            name='znesek',
            field=models.DecimalField(decimal_places=2, max_digits=8, default='0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stranka',
            name='skupaj_prodano',
            field=models.DecimalField(decimal_places=2, max_digits=9),
            preserve_default=True,
        ),
    ]
