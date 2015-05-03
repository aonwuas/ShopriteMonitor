# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reader', '0004_store_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='circular',
            field=models.ForeignKey(default=1, to='Reader.Circular'),
            preserve_default=False,
        ),
    ]
