from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from openpyxl import load_workbook

from django.db.models.functions import Concat


# Create your models here.


class AuctionHouse(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos')

    def __str__(self):
        return f'{self.name} | {self.city}'


class Auction(models.Model):
    auction_house = models.ForeignKey(AuctionHouse, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200)
    file = models.FileField(upload_to='auctions')

    __original_file = None

    def __str__(self):
        return f'{self.auction_house} | {self.slug}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_file = self.file

    def save(self, *args, **kwargs):
        process_excel = False
        if self.__original_file is None or self.__original_file != self.file:
            process_excel = True

        super().save(*args, **kwargs)

        if process_excel:
            self.process_excel()

    def process_excel(self):
        # delete previous items in the auction
        AuctionItem.objects.filter(auction=self).delete()

        wb = load_workbook(self.file.path)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, max_col=6, max_row=ws.max_row):
            ai = AuctionItem.objects.create(
                auction=self,
                lot=row[0].value,
                title=row[1].value,
                tier=row[2].value,
                description=row[3].value,
                product_url=row[4].value,
                photos_url=row[5].value,
            )
            ai.save()


class AuctionItem(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    lot = models.CharField(max_length=100)
    title = models.TextField(blank=True, null=True)
    tier = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product_url = models.URLField(blank=True, null=True)
    photos_url = models.URLField(blank=True, null=True)

    search_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.search_name}'

    def save(self, *args, **kwargs):
        if not self.search_name:
            self.search_name = f'{self.lot} | {self.title}'
        super(AuctionItem, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']
