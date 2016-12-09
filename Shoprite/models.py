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
class StaticItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=128)


class SaleItem(models.Model):
    static_item = models.ForeignKey(StaticItem)
    circular = models.ForeignKey(Circular)
    card_requirement = models.BooleanField(default=False)


class ConditionalSale(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    buy = models.IntegerField()
    get = models.IntegerField()


class Units(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    unit = models.CharField(max_length=8)


class FlatPriceSale(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class XForYSale(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    effective_price = models.DecimalField(max_digits=6, decimal_places=2)


class FractionalReductionSale(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    percent_reduction = models.IntegerField()
    fractional_reduction = models.CharField(max_length=16)


class PercentReductionSale(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    percent_reduction = models.IntegerField()


class RangedPriceSale(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    minimum_price = models.DecimalField(max_digits=6, decimal_places=2)
    maximum_price = models.DecimalField(max_digits=6, decimal_places=2)


class FlatReductionSale(models.Model):
    sale_item = models.ForeignKey(SaleItem)
    price_reduction = models.DecimalField(max_digits=6, decimal_places=2)