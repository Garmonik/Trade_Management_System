from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=False)
    location = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Market(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    amount = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.place} - {self.product}'


class Storage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.place} - {self.product}'


class Selling(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    amount = models.IntegerField(null=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.place} - {self.product}'