from django.shortcuts import render
from django.db.models import Q

from phonenumber_field.phonenumber import PhoneNumber

from quotes.models import Quote

import logging

logger = logging.getLogger('other_file')


def index(request, phone_number):
    formatted_number = PhoneNumber.from_string(phone_number)

    quotes = Quote.objects.filter(
        Q(bill_to_phone=formatted_number)
        | Q(designer_phone=formatted_number)
        | Q(from_phone=formatted_number)
        | Q(to_phone=formatted_number)
    ).order_by('status')

    context = {
        'phone_number': formatted_number,
        'quotes': quotes,
    }

    return render(request, 'account/index.html', context)
