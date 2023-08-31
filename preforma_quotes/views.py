from django.shortcuts import render
from .forms import ToAddressForm, FromAddressForm


# Create your views here.
def quote(request):
    to_address = ToAddressForm()
    from_address = FromAddressForm()

    options = [
        {'value': 1, 'name': 'Robert Gordy, (American/Louisiana, 1933-1986), "By The Sea", 1977, Acrylic On Canvas'},
        {'value': 2, 'name': 'Robert Gordy, (American/Louisiana, 1933-1986), "Nude In The Woods", Marker On Paper'},
        {'value': 3, 'name': 'Robert Gordy, (American/Louisiana, 1933-1986), "Folly", 1980, Screen Print'},
        {'value': 4, 'name': 'Jere Hardy Allen, (American/Mississippi, B. 1944), "Muses", Oil On Linen'},
        {'value': 5, 'name': 'Will Hinds, (American/Louisiana, 1936-2014), "Nobody\'s Home", Tempera On Board'},
        {'value': 6, 'name': 'Chris Roberts-Antieau, (American, B. 1951), "Horseback Rider", Embroidered Cloth'},
        {'value': 7, 'name': 'Charles Schorre, (American/Texas, 1925-1996), "Untitled: Abstraction", 1971, Acrylic On Paper'},
        {'value': 8, 'name': 'James Michalopoulos, (American/Louisiana, B. 1951), "Just Riley\'s", Oil On Canvas'},
        {'value': 9, 'name': 'George Rodrigue, (American/Louisiana, 1944-2013), "Blue Dog With Cypress Trees", 1994, Cameo Glass'},
        {'value': 10, 'name': 'George Rodrigue, (American/Louisiana, 1944-2013), "I Walk The Line", 2003, Silkscreen'},
    ]
    context = {
        'options': options,
        'to_address': to_address,
        'from_address': from_address,
    }
    return render(request, 'preforma-quotes/quote-form.html', context)
