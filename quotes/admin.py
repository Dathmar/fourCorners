from django.contrib import admin
from .models import Quote, QuoteOptions, QuoteItem, QuoteBol


# Register your models here.
class QuoteOptionsInline(admin.TabularInline):
    model = QuoteOptions


class QuoteBolInline(admin.TabularInline):
    model = QuoteBol
    extra = 1


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('encoding', 'bill_to_name', 'bill_to_email', 'bill_to_phone', 'status', 'number_of_items', )

    inlines = [QuoteOptionsInline, QuoteBolInline]


@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):
    list_display = ('get_quote_encoding', 'get_bill_to_name', 'item_id', 'get_item_description', 'label', )

    def get_bill_to_name(self, obj):
        return obj.quote.bill_to_name

    def get_item_description(self, obj):
        return obj.item.description

    def get_quote_encoding(self, obj):
        return obj.quote.encoding
