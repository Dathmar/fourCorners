from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_select2 import forms as s2forms

from .models import AuctionItem


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


class OptionsWidget(s2forms.Select2MultipleWidget):
    css_class_name = 'w-100 django-select2'
    search_fields = [
        "search_name__icontains",
    ]


class OptionsForm(forms.Form):
    options = forms.MultipleChoiceField(
        widget=OptionsWidget,
        label=False,
    )

    def clean_options(self):
        options = self.cleaned_data['options']
        if not options:
            raise forms.ValidationError('Please select at least one item.')
        options = [int(x) for x in options]
        return options
