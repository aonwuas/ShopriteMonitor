# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shoprite', '0010_flatreductionitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConditionalSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buy', models.IntegerField()),
                ('get', models.IntegerField()),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.CreateModel(
            name='FlatPriceSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.CreateModel(
            name='FlatReductionSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_reduction', models.DecimalField(max_digits=6, decimal_places=2)),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.CreateModel(
            name='FractionalReductionSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent_reduction', models.IntegerField()),
                ('fractional_reduction', models.CharField(max_length=16)),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.CreateModel(
            name='PercentReductionSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent_reduction', models.IntegerField()),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.CreateModel(
            name='RangedPriceSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum_price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('maximum_price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.CreateModel(
            name='XForYSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('effective_price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('sale_item', models.ForeignKey(to='Shoprite.SaleItem')),
            ],
        ),
        migrations.RenameModel(
            old_name='Item',
            new_name='StaticItem',
        ),
        migrations.RemoveField(
            model_name='conditional',
            name='sale_item',
        ),
        migrations.RemoveField(
            model_name='flatpriceitem',
            name='sale_item',
        ),
        migrations.RemoveField(
            model_name='flatreductionitem',
            name='sale_item',
        ),
        migrations.RemoveField(
            model_name='fractionalreductionitem',
            name='sale_item',
        ),
        migrations.RemoveField(
            model_name='percentreductionitem',
            name='sale_item',
        ),
        migrations.RemoveField(
            model_name='rangedpriceitem',
            name='sale_item',
        ),
        migrations.RemoveField(
            model_name='xforyitem',
            name='sale_item',
        ),
        migrations.DeleteModel(
            name='Conditional',
        ),
        migrations.DeleteModel(
            name='FlatPriceItem',
        ),
        migrations.DeleteModel(
            name='FlatReductionItem',
        ),
        migrations.DeleteModel(
            name='FractionalReductionItem',
        ),
        migrations.DeleteModel(
            name='PercentReductionItem',
        ),
        migrations.DeleteModel(
            name='RangedPriceItem',
        ),
        migrations.DeleteModel(
            name='XForYItem',
        ),
    ]
