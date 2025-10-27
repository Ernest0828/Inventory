from django.db import models

# Create your models here.
class Items(models.Model):
    item_name = models.CharField(max_length=200)
    item_id = models.CharField(max_length=100, null=True, blank=True)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.item_name} - {self.item_id} - {self.stock}"
