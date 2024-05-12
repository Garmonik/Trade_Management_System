import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Admin(User):
    access_key = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class AdminSettings(models.Model):
    user = models.OneToOneField(Admin, on_delete=models.CASCADE, primary_key=True, related_name='user_settings', db_index=True)
    date_min = models.IntegerField(null=True, blank=True, default=7)
    percent_min = models.PositiveIntegerField(blank=True, default=7)
    data_max = models.IntegerField(null=True, blank=True, default=7)
    percent_max = models.PositiveIntegerField(default=7, blank=True)
    count_min = models.PositiveIntegerField(default=7, blank=True)
    count_max = models.PositiveIntegerField(default=7, blank=True)
    write_off_date = models.IntegerField(null=True, blank=True, default=7)
    minimum_quantity_of_goods = models.PositiveIntegerField(default=7, blank=True)

    class Meta():
        verbose_name = 'AdminSettings'


@receiver(post_save, sender=Admin)
def create_profile_settings(sender, instance, created, **kwargs):
    if created:
        AdminSettings(user=instance)._save_table(cls=AdminSettings)


class Product(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=False)
    type_product = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name


class Place(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=False)
    location = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Market(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    amount = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.product.name}'


class MarketUpdate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class Storage(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.place} - {self.product}'


class Selling(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    amount = models.IntegerField(null=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.place} - {self.product}'