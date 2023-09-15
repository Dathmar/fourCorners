from django.db import models


# Create your models here.
class Item(models.Model):
    quantity = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=None, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description



