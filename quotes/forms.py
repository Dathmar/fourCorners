from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import QuoteOptions


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
            'placeholder': 'Delivery Contact Email'})
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
    ref_number = forms.CharField(
        max_length=1000,
        label=False,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Reference/Order#'})
    )


class ContactForm(forms.Form):
    bill_to_name = forms.CharField(
        max_length=1000,
        label='Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Bill to Name'})
    )
    bill_to_phone = PhoneNumberField(
        max_length=20,
        label='Phone',
        region='US',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Bill to Phone'})
    )
    bill_to_email = forms.EmailField(
        max_length=1000,
        label=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Bill To Email'})
    )
    designer_name = forms.CharField(
        max_length=1000,
        label=False,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Designer Name (optional)'})
    )
    designer_phone = PhoneNumberField(
        max_length=20,
        label=False,
        required=False,
        region='US',
        widget=forms.TextInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Designer Phone Number (optional)'})
    )
    designer_email = forms.EmailField(
        max_length=1000,
        label=False,
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Designer Email (optional)'})
    )


class OptionsForm(forms.Form):
    delivery_type = forms.CharField(
        max_length=20,
        label=False,
        widget=forms.Select(
            choices=(
                ('Curbside', 'Curbside'),
                ('White Glove', 'White Glove'),
                ('White Glove Wrap', 'White Glove | Professional Wrapping Required'),
                ('Front Door', 'Threshold | Front Door or Garage'),
            ),
            attrs={
                'class': 'form-control-sm w-100',
            }
        )
    )
    delivery_notes = forms.CharField(
        max_length=1000,
        label=False,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control-sm w-100',
            'placeholder': 'Tell us about the delivery requirements:\nIs it a limit access address (gate code), are there stairs, do you need assembly... '}
        )
    )

    def clean_options(self):
        data = self.cleaned_data['options']
        if isinstance(data, str):
            return [data]

        return data


class ItemForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control-sm w-100',
                'placeholder': 'Quantity',
            }
        )
    )
    description = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-sm w-100',
                'placeholder': 'Description',
            }
        )
    )
    weight = forms.DecimalField(
        required=False,
        max_digits=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-sm w-100',
                'placeholder': 'Weight (lbs)',
            }
        )
    )
    length = forms.DecimalField(
        required=False,
        max_digits=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-sm w-100',
                'placeholder': 'Length (in)',
            }
        )
    )
    width = forms.DecimalField(
        required=False,
        max_digits=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-sm w-100',
                'placeholder': 'Width (in)',
            }
        )
    )
    height = forms.DecimalField(
        required=False,
        max_digits=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-sm w-100',
                'placeholder': 'Height (in)',
            }
        )
    )


