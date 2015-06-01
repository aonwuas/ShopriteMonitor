# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0009_auto_20150601_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatReductionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_reduction', models.DecimalField(max_digits=6, decimal_places=2)),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
    ]
