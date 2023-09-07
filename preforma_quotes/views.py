from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from .forms import ToAddressForm, OptionsForm

import logging

logger = logging.getLogger('other_file')


# Create your views here.
def quote(request, auction_slug):
    slug_list = [
        'new-orleans',
        'vogt',
        'hindman',
        'austin-auction',
        'neal-auction',
        'crescent-city',
        'bright-star',
        'ms-rau',
        'hill-country-interiors',
    ]

    if auction_slug not in slug_list:
        raise Http404("Auction not found")

    logo_address = {
        'new-orleans': {
            'logo': '/media/logos/New Orleans Auction Gallery.png',
            'address': 'New Orleans Auction Gallery<br>333 St Joseph St<br>New Orleans, LA 70130<br>(504) 566-1849<br>'
        },
        'vogt': {
            'logo': '/media/logos/Vogt Auction Gallery.png',
            'address': 'Vogt Auction<br>7233 Blanco Rd<br>San Antonio, TX 78216<br>(210) 822-6155<br>'
        },
        'hindman': {
            'logo': '/media/logos/Hindman Auctions.png',
            'address': 'Hindman<br>1550 W Carroll Ave<br>Chicago, IL 60607<br>(312) 280-1212'
        },
        'austin-auction': {
            'logo': '/media/logos/Austin Auction Gallery.png',
            'address': 'Austin Auction Gallery<br>8414 Anderson Mill Rd<br>Austin, TX 78729<br>(512) 258-5479'
        },
        'neal-auction': {
            'logo': '/media/logos/Neal Auction.png',
            'address': 'Neal Auction<br>4038 Magazine St<br>New Orleans, LA 70115<br>(504) 899-5329'
        },
        'crescent-city': {
            'logo': '/media/logos/Crescent City.png',
            'address': 'Crescent City Auction<br>1330 St Charles Ave<br>New Orleans, LA 70130<br>(504) 529-5057'
        },
        'bright-star': {
            'logo': '/media/logos/Bright Star Antiques Auction.png',
            'address': 'Bright Star Antiques Auction<br>1205 Main St<br>Sulphur Springs, TX 75482<br>(903) 885-4584'
        },
        'ms-rau': {
            'logo': '/media/logos/MS Rau.png',
            'address': 'M.S. Rau<br>622 Royal St<br>New Orleans, LA 70130<br>(888) 711-8084'
        },
        'hill-country-interiors': {
            'logo': '/media/logos/Hill Country Interiors.png',
            'address': 'Hill Country Interiors<br>1410 N Loop 1604 W<br>San Antonio, TX 78248<br>(210) 495-5768'
        },


    }

    if request.method == 'POST':
        to_address = ToAddressForm(request.POST)
        options_form = OptionsForm(request.POST)

        if to_address.is_valid() and options_form.is_valid():
            option_choices = [
                (1, 'Lot 105 | Robert Gordy, (American/Louisiana, 1933-1986), "By The Sea", 1977, Acrylic On Canvas'),
                (2, 'Lot 106 | Robert Gordy, (American/Louisiana, 1933-1986), "Nude In The Woods", Marker On Paper'),
                (3, 'Lot 107 | Robert Gordy, (American/Louisiana, 1933-1986), "Folly", 1980, Screen Print'),
                (4, 'Lot 108 | Jere Hardy Allen, (American/Mississippi, B. 1944), "Muses", Oil On Linen'),
                (5, 'Lot 109 | Will Hinds, (American/Louisiana, 1936-2014), "Nobody\'s Home", Tempera On Board'),
                (6, 'Lot 110 | Chris Roberts-Antieau, (American, B. 1951), "Horseback Rider", Embroidered Cloth'),
                (7,
                 'Lot 111 | Charles Schorre, (American/Texas, 1925-1996), "Untitled: Abstraction", 1971, Acrylic On Paper'),
                (8, 'Lot 112 | James Michalopoulos, (American/Louisiana, B. 1951), "Just Riley\'s", Oil On Canvas'),
                (9,
                 'Lot 113 | George Rodrigue, (American/Louisiana, 1944-2013), "Blue Dog With Cypress Trees", 1994, Cameo Glass'),
                (10, 'Lot 114 | George Rodrigue, (American/Louisiana, 1944-2013), "I Walk The Line", 2003, Silkscreen'),
            ]
            selected_options = options_form.cleaned_data
            logger.info(f'selected_options: {selected_options}')
            option_thing = []
            for option_choice in option_choices:
                if str(option_choice[0]) in selected_options['options']:
                    option_thing.append(option_choice)

            context = {
                'option_thing': option_thing,
                'address': logo_address[auction_slug]['address'],
                'logo': logo_address[auction_slug]['logo'],
                'square_js_url': settings.SQUARE_JS_URL
            }
            return render(request, 'preforma-quotes/quote-price.html', context)

    else:
        to_address = ToAddressForm()
        options_form = OptionsForm()

    context = {
        'options_form': options_form,
        'to_address': to_address,
        'address': logo_address[auction_slug]['address'],
        'logo': logo_address[auction_slug]['logo'],
    }
    return render(request, 'preforma-quotes/quote-form.html', context)
