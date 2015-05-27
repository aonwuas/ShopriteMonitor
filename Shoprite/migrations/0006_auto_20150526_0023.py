# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0005_item_circular'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPriceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='FractionalReductionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fractional_reduction', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PercentReductionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent_reduction', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RangedPriceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum_price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('maximum_price', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card_requirement', models.BooleanField(default=False)),
                ('circular', models.ForeignKey(to='Shoprite.Circular')),
            ],
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit', models.CharField(max_length=255)),
                ('item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.CreateModel(
            name='XForYItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('effective_price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.RemoveField(
            model_name='sale',
            name='item',
        ),
        migrations.RemoveField(
            model_name='item',
            name='circular',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
        migrations.AddField(
            model_name='saleitem',
            name='static_item',
            field=models.ForeignKey(to='Shoprite.Item'),
        ),
        migrations.AddField(
            model_name='rangedpriceitem',
            name='sale_item',
            field=models.ForeignKey(to='Shoprite.SaleItem'),
        ),
        migrations.AddField(
            model_name='percentreductionitem',
            name='sale_item',
            field=models.ForeignKey(to='Shoprite.SaleItem'),
        ),
        migrations.AddField(
            model_name='fractionalreductionitem',
            name='sale_item',
            field=models.ForeignKey(to='Shoprite.SaleItem'),
        ),
        migrations.AddField(
            model_name='flatpriceitem',
            name='sale_item',
            field=models.ForeignKey(to='Shoprite.SaleItem'),
        ),
    ]
