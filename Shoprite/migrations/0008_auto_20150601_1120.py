# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0007_auto_20150601_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='fractionalreductionitem',
            name='percent_reduction',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fractionalreductionitem',
            name='fractional_reduction',
            field=models.CharField(max_length=16),
        ),
    ]
