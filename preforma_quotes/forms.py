from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_select2 import forms as s2forms


class ToAddressForm(forms.Form):
    to_name = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Contact Name'})
    )
    to_street = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Street'})
    )
    to_city = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'City'})
    )
    to_state = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'State'})
    )
    to_zip = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Zip'})
    )
    to_phone = PhoneNumberField(
        max_length=20,
        label=False,
        region='US',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Phone Number'})
    )
    to_email = forms.EmailField(
        max_length=1000,
        label=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Contact Email'})
    )


class FromAddressForm(forms.Form):
    from_name = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Contact Name'})
    )
    from_street = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Street'})
    )
    from_city = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'City'})
    )
    from_state = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'State'})
    )
    from_zip = forms.CharField(
        max_length=1000,
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Zip'})
    )
    from_phone = PhoneNumberField(
        max_length=20,
        label=False,
        region='US',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Phone Number'})
    )
    from_email = forms.EmailField(
        max_length=1000,
        label=False,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Pickup Contact Email'})
    )


class OptionsForm(forms.Form):
    option_choices = [
        (1,'Lot 105 | Robert Gordy, (American/Louisiana, 1933-1986), "By The Sea", 1977, Acrylic On Canvas'),
        (2, 'Lot 106 | Robert Gordy, (American/Louisiana, 1933-1986), "Nude In The Woods", Marker On Paper'),
        (3, 'Lot 107 | Robert Gordy, (American/Louisiana, 1933-1986), "Folly", 1980, Screen Print'),
        (4, 'Lot 108 | Jere Hardy Allen, (American/Mississippi, B. 1944), "Muses", Oil On Linen'),
        (5, 'Lot 109 | Will Hinds, (American/Louisiana, 1936-2014), "Nobody\'s Home", Tempera On Board'),
        (6, 'Lot 110 | Chris Roberts-Antieau, (American, B. 1951), "Horseback Rider", Embroidered Cloth'),
        (7, 'Lot 111 | Charles Schorre, (American/Texas, 1925-1996), "Untitled: Abstraction", 1971, Acrylic On Paper'),
        (8, 'Lot 112 | James Michalopoulos, (American/Louisiana, B. 1951), "Just Riley\'s", Oil On Canvas'),
        (9, 'Lot 113 | George Rodrigue, (American/Louisiana, 1944-2013), "Blue Dog With Cypress Trees", 1994, Cameo Glass'),
        (10, 'Lot 114 | George Rodrigue, (American/Louisiana, 1944-2013), "I Walk The Line", 2003, Silkscreen'),
    ]
    options = forms.MultipleChoiceField(choices=option_choices, widget=s2forms.Select2MultipleWidget(), label=False)
