from django.db import models
# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    locale = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=40)


class Circular(models.Model):
    store = models.ForeignKey(Store)
    start = models.DateField()
    end = models.DateField()


class Item(models.Model):
    # circular = models.ForeignKey(Circular)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.CharField(max_length=255)


class Sale(models.Model):
    item = models.ForeignKey(Item)
    name = models.CharField(max_length=255)