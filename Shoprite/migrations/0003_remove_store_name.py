# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0002_store_locale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='name',
        ),
    ]
