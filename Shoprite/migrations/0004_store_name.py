# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0003_remove_store_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='name',
            field=models.CharField(default='temp', unique=True, max_length=255),
            preserve_default=False,
        ),
    ]
