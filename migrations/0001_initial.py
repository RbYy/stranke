# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Obisk',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('datum', models.DateField()),
                ('znesek', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Produkt',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=32)),
                ('okrajsava', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stranka',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('podjetje', models.CharField(max_length=100)),
                ('naslov', models.CharField(max_length=100)),
                ('kraj', models.CharField(max_length=30)),
                ('oseba', models.CharField(max_length=100)),
                ('skupaj_prodano', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='produkt',
            name='skladisce',
            field=models.ManyToManyField(to='stranke4.Stranka'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obisk',
            name='demo',
            field=models.ManyToManyField(related_name='demo', to='stranke4.Produkt'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obisk',
            name='prodaja',
            field=models.ManyToManyField(related_name='prodaja', to='stranke4.Produkt'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obisk',
            name='stranka',
            field=models.ForeignKey(to='stranke4.Stranka'),
            preserve_default=True,
        ),
    ]
