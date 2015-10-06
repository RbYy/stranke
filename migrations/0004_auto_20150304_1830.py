# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stranke4', '0003_auto_20150304_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stranka',
            name='naslov',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stranka',
            name='oseba',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
