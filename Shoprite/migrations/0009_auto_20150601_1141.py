# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0008_auto_20150601_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conditional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buy', models.IntegerField()),
                ('get', models.IntegerField()),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='units',
            name='unit',
            field=models.CharField(max_length=8),
        ),
    ]
