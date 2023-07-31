from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.shortcuts import reverse
from django.conf import settings

import quotes.quote_emails as quote_emails

import base62
import uuid
import logging

from random import getrandbits
from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger('other_file')


# Create your models here.
class Quote(models.Model):
    QUOTE_STATUS_CHOICES = (
        ('send_created_notification', 'Send Created Notification'),
        ('created', 'Created'),
        ('send_options_notification', 'Send Options Notification'),
        ('options_notification_sent', 'Options Notification Sent'),
        ('needs_payment', 'Needs Payment'),
        ('resend_payment_notification', 'Resend Payment Notification'),
        ('paid', 'Paid'),
        ('send_bol_notification', 'Send BOL Notification'),
        ('bol_notification_sent', 'BOL Notification Sent'),
        ('shipped', 'Shipped'),
        ('send_delivery_notification', 'Send Delivery Notification'),
        ('delivered', 'Delivered'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    to_name = models.CharField(max_length=1000)
    to_email = models.EmailField(max_length=1000)
    to_phone = PhoneNumberField()
    to_street = models.CharField(max_length=1000)
    to_city = models.CharField(max_length=1000)
    to_state = models.CharField(max_length=1000)
    to_zip = models.CharField(max_length=1000)

    from_name = models.CharField(max_length=1000)
    from_phone = PhoneNumberField()
    from_street = models.CharField(max_length=1000)
    from_city = models.CharField(max_length=1000)
    from_state = models.CharField(max_length=1000)
    from_zip = models.CharField(max_length=1000)
    from_email = models.EmailField(blank=True, null=True)

    reference_number = models.CharField(max_length=1000,  blank=True, null=True)

    bill_to_name = models.CharField(max_length=1000)
    bill_to_email = models.EmailField(max_length=1000)
    bill_to_phone = PhoneNumberField(blank=True, null=True)

    designer_name = models.CharField(max_length=1000, blank=True, null=True)
    designer_email = models.EmailField(max_length=1000, blank=True, null=True)
    designer_phone = PhoneNumberField(blank=True, null=True)

    delivery_type = models.CharField(max_length=1000)
    delivery_notes = models.CharField(max_length=1000, blank=True, null=True)

    encoding = models.CharField(max_length=10, blank=True, null=True)

    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    status = models.CharField(max_length=30, choices=QUOTE_STATUS_CHOICES, default='created')

    pickup_window = models.CharField(max_length=1000, blank=True, null=True)
    delivery_window = models.CharField(max_length=1000, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.encoding:
            self.encoding = self.generate_unique_encoding()

        if self.status == 'send_created_notification':
            self.status = 'created'
            quote_emails.send_create_external_email(self)
            quote_emails.send_internal_email(self)
        elif self.status == 'send_options_notification':
            self.status = 'options_notification_sent'
            quote_emails.send_quote_options_external_email(self)
            quote_emails.send_internal_email(self)
        elif self.status in ('paid', 'resend_payment_notification'):
            self.status = 'paid'
            quote_emails.send_quote_paid_external_email(self)
            quote_emails.send_internal_email(self)
        elif self.status == 'send_bol_notification':
            self.status = 'bol_notification_sent'
            quote_emails.send_quote_label_external_email(self)
            quote_emails.send_internal_email(self)
        elif self.status == 'send_delivery_notification':
            self.status = 'delivered'
            quote_emails.send_delivered_external_email(self)
            quote_emails.send_internal_email(self)

        super().save(*args, **kwargs)

    def generate_unique_encoding(self):
        while True:
            base = base62.encodebytes(self.id.bytes + getrandbits(8).to_bytes(1, 'big'))
            base = base[:6].zfill(6)
            if not Quote.objects.filter(encoding=base).exists():
                return base

    def get_cost(self):
        selected_option = QuoteOptions.objects.filter(quote=self.id, selected_option=True)
        if selected_option.exists():
            return selected_option.first().option_price
        return None

    def get_square_charge(self):
        cost = self.get_cost()
        if cost:
            return int(cost) * 100
        return None

    def get_from_info(self):
        from_info = {
            'name': self.from_name,
            'street': self.from_street,
            'city': self.from_city,
            'state': self.from_state,
            'zip': self.from_zip,
            'phone': str(self.from_phone),
            'email': self.from_email,
            'ref_number': self.reference_number,
        }
        return from_info

    def get_to_info(self):
        to_info = {
            'name': self.to_name,
            'street': self.to_street,
            'city': self.to_city,
            'state': self.to_state,
            'zip': self.to_zip,
            'phone': str(self.to_phone),
            'email': self.to_email,
        }
        return to_info

    def get_bill_to_info(self):
        bill_to_info = {
            'name': self.bill_to_name,
            'phone': str(self.bill_to_phone),
            'email': self.bill_to_email,
        }
        return bill_to_info

    def get_designer_info(self):
        designer_info = {
            'name': self.designer_name,
            'phone': str(self.designer_phone),
            'email': self.designer_email,
        }
        return designer_info

    def get_options_info(self):
        options_info = {
            'delivery_type': self.delivery_type,
            'delivery_notes': self.delivery_notes,
        }
        return options_info

    def get_items_in_quote(self):
        items = []
        for item in QuoteItem.objects.filter(quote=self.id):
            items.append({
                'quantity': str(item.item.quantity),
                'description': item.item.description,
                'weight': str(item.item.weight),
                'length': str(item.item.length),
                'width': str(item.item.width),
                'height': str(item.item.height),
                'value': str(item.item.value)
            })
        return items

    def get_quote_options_url(self):
        return settings.BASE_URL + reverse('quotes:option-select', args=[self.encoding])

    def get_label_url(self):
        return settings.BASE_URL + reverse('quotes:labels', args=[self.encoding])


def quote_label_upload(instance, filename):
    return f'labels/{instance.quote.id}/{filename}'


class QuoteBol(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    bol = models.FileField(upload_to=quote_label_upload, blank=True, null=True)


class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
    label = models.FileField(upload_to=quote_label_upload, blank=True, null=True)

    def __str__(self):
        return f'{self.quote.encoding} | {self.item.description}'


class QuoteOptions(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    option_description = models.CharField(max_length=1000)
    option_price = models.DecimalField(max_digits=10, decimal_places=2)
    selected_option = models.BooleanField(default=False)

    def __str__(self):
        return self.option_description

