from django.db import models


# Create your models here.
class Item(models.Model):
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=2)
    length = models.DecimalField(max_digits=15, decimal_places=2)
    width = models.DecimalField(max_digits=15, decimal_places=2)
    height = models.DecimalField(max_digits=15, decimal_places=2)
    value = models.DecimalField(max_digits=15, decimal_places=2, default=None, null=True)

    box = models.ForeignKey('preforma_quotes.Box', on_delete=models.CASCADE, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description



