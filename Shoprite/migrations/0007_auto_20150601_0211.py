# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0006_auto_20150526_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='units',
            old_name='item',
            new_name='sale_item',
        ),
    ]
