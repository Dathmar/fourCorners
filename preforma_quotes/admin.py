from django.contrib import admin

from .models import AuctionHouse, Auction, AuctionItem, Box


@admin.register(AuctionItem)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('auction', 'search_name', 'box')
    list_filter = ['auction']


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'max_item_length', 'max_item_width', 'max_item_height')
    list_editable = ('description', 'max_item_length', 'max_item_width', 'max_item_height')


# Register your models here.
admin.site.register(AuctionHouse)
admin.site.register(Auction)
