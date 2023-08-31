from django import forms
from phonenumber_field.formfields import PhoneNumberField


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