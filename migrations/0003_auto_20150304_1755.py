# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stranke4', '0002_stranka_uporabnik'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stranka',
            name='naslov',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stranka',
            name='oseba',
            field=models.CharField(blank=True, max_length=100),
            preserve_default=True,
        ),
    ]
