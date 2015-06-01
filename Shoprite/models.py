from django.db import models
# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    locale = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=40)


class Circular(models.Model):
    store = models.ForeignKey(Store)
    start = models.DateField()
    end = models.DateField()


# Static item
class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)


class SaleItem(models.Model):
    static_item = models.ForeignKey(Item)
    circular = models.ForeignKey(Circular)
    card_requirement = models.BooleanField(default=False)


class Units(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    unit = models.CharField(max_length=255)


class FlatPriceItem(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class XForYItem(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    effective_price = models.DecimalField(max_digits=6, decimal_places=2)


class FractionalReductionItem(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    fractional_reduction = models.CharField(max_length=255)


class PercentReductionItem(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    percent_reduction = models.IntegerField()


class RangedPriceItem(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    minimum_price = models.DecimalField(max_digits=6, decimal_places=2)
    maximum_price = models.DecimalField(max_digits=6, decimal_places=2)


"""
class FlatReductionItem(SaleItem):
    sale_item = models.ForeignKey(SaleItem)
    price_reduction = models.DecimalField(max_digits=None, decimal_places=2)
"""