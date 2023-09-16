from django.contrib import admin

from .models import AuctionHouse, Auction, AuctionItem


# Register your models here.
admin.site.register(AuctionHouse)
admin.site.register(Auction)
admin.site.register(AuctionItem)
