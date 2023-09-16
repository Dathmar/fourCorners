from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import Http404, HttpResponseRedirect

from .forms import ToAddressForm, OptionsForm
from .models import Auction, AuctionItem
from quotes.helpers import generate_quote_objects_in_db

import logging

logger = logging.getLogger('other_file')


# Create your views here.
def select_items(request, auction_slug):
    auction = get_object_or_404(Auction, slug=auction_slug)
    auction_address = (f'{auction.auction_house.name}<br>{auction.auction_house.address}'
                       f'<br>{auction.auction_house.city}, {auction.auction_house.state} '
                       f'{auction.auction_house.zip_code}<br>{auction.auction_house.phone_number}')

    if request.method == 'POST':
        to_address = ToAddressForm(request.POST)
        options_form = OptionsForm(request.POST)
        options_form.fields['options'].queryset = AuctionItem.objects.filter(auction=auction)

        logger.info(request.POST)

        if to_address.is_valid() and options_form.is_valid():
            options = options_form.cleaned_data['options']

            request.session[auction_slug] = {
                'to_address': {
                    'to_name': to_address.cleaned_data['to_name'],
                    'to_street': to_address.cleaned_data['to_street'],
                    'to_city': to_address.cleaned_data['to_city'],
                    'to_state': to_address.cleaned_data['to_state'],
                    'to_zip': to_address.cleaned_data['to_zip'],
                    'to_phone': str(to_address.cleaned_data['to_phone']),
                    'to_email': to_address.cleaned_data['to_email']
                },
                'options': options
            }

            # create normal quote as create status
            auction_items = AuctionItem.objects.filter(id__in=options)

            # get individual values
            from_info = {
                'name': auction.auction_house.name,
                'street': auction.auction_house.address,
                'city': auction.auction_house.city,
                'state': auction.auction_house.state,
                'zip': auction.auction_house.zip_code,
                'email': auction.auction_house.email,
                'phone': auction.auction_house.phone_number,
                'ref_number': ""
            }

            to_info = {
                'name': to_address.cleaned_data['to_name'],
                'street': to_address.cleaned_data['to_street'],
                'city': to_address.cleaned_data['to_city'],
                'state': to_address.cleaned_data['to_state'],
                'zip': to_address.cleaned_data['to_zip'],
                'phone': str(to_address.cleaned_data['to_phone']),
                'email': to_address.cleaned_data['to_email']
            }

            items = []
            for item_form in auction_items:
                item = {
                    'quantity': 1,
                    'description': item_form.description,
                    'weight': 0,
                    'length': 0,
                    'width': 0,
                    'height': 0,
                    'value': 0,
                }
                items.append(item)

            bill_to_info = {
                'name': to_address.cleaned_data['to_name'],
                'phone': str(to_address.cleaned_data['to_phone']),
                'email': to_address.cleaned_data['to_email'],
            }

            designer_info = {
                'name': None,
                'phone': None,
                'email': None,
            }

            options_info = {
                'delivery_type': 'Front Door',
                'delivery_notes': None,
            }

            quote_obj = generate_quote_objects_in_db(
                from_info, to_info, bill_to_info, items, designer_info, options_info
            )

            return redirect('preforma-quotes:quote', auction_slug=auction_slug)
    else:
        previous_options = None
        previous_to_address = None

        to_address = ToAddressForm()
        options_form = OptionsForm()
        options_form.fields['options'].queryset = AuctionItem.objects.filter(auction=auction)

        # get existing quote in the session if it exists
        if request.session.get(auction_slug, None):
            previous_options = request.session[auction_slug].get('options', None)
            previous_to_address = request.session[auction_slug].get('to_address', None)

        if previous_options:
            options_form.fields['options'].initial = previous_options

        if previous_to_address:
            to_address.fields['to_name'].initial = previous_to_address.get('to_name', None)
            to_address.fields['to_street'].initial = previous_to_address.get('to_street', None)
            to_address.fields['to_city'].initial = previous_to_address.get('to_city', None)
            to_address.fields['to_state'].initial = previous_to_address.get('to_state', None)
            to_address.fields['to_zip'].initial = previous_to_address.get('to_zip', None)
            to_address.fields['to_phone'].initial = previous_to_address.get('to_phone', None)
            to_address.fields['to_email'].initial = previous_to_address.get('to_email', None)

    context = {
        'options_form': options_form,
        'to_address': to_address,
        'address': auction_address,
        'logo': f'/media/{auction.auction_house.logo}',
    }
    return render(request, 'preforma-quotes/quote-form.html', context)


def quote(request, auction_slug):
    auction = get_object_or_404(Auction, slug=auction_slug)
    auction_address = (f'{auction.auction_house.name}<br>{auction.auction_house.address}'
                       f'<br>{auction.auction_house.city}, {auction.auction_house.state} '
                       f'{auction.auction_house.zip_code}<br>{auction.auction_house.phone_number}')

    if request.session.get(auction_slug, None):
        previous_options = request.session[auction_slug].get('options', None)
        previous_to_address = request.session[auction_slug].get('to_address', None)
    else:
        raise Http404('Quote information not found')

    if request.session.get(auction_slug, None):
        previous_options = request.session[auction_slug].get('options', None)
        previous_to_address = request.session[auction_slug].get('to_address', None)

    if previous_options:
        previous_options = AuctionItem.objects.filter(pk__in=previous_options)
    else:
        raise Http404('Item information not found')

    if previous_to_address:
        address = f'{previous_to_address.get("to_name")}<br>'
        address += f'{previous_to_address.get("to_street")}<br>'
        address += f'{previous_to_address.get("to_city")},'
        address += f'{previous_to_address.get("to_state")}'
        address += f'{previous_to_address.get("to_zip")}<br>'
        address += f'{previous_to_address.get("to_phone")}<br>'
        address += f'{previous_to_address.get("to_email")}'
    else:
        raise Http404('Delivery information not found')

    context = {
        'address': address,
        'logo': f'/media/{auction.auction_house.logo}',
        'options': previous_options,
        'auction_address': auction_address,
    }
    request.session[auction_slug] = None
    return render(request, 'preforma-quotes/quote-price.html', context)


def clear(request, auction_slug):
    if request.session.get(auction_slug, None):
        del request.session[auction_slug]
    return HttpResponseRedirect(reverse('preforma-quotes:quote-form', args=[auction_slug]))


def blah(request):
    auction_items = AuctionItem.objects.all()

    for auction_item in auction_items:
        auction_item.search_name = ''
        auction_item.save()
