from django.db import models

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    price = models.IntegerField()
    name = models.CharField()

    def __str__(self):
        return self.name
