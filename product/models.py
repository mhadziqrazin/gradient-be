from django.db import models

class Product(models.Model):
    price = models.IntegerField()
    name = models.CharField()

    def __str__(self):
        return self.name
