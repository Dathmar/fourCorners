from datetime import datetime

from django.shortcuts import render, redirect
from django.conf import settings
from django.forms.formsets import formset_factory
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.apps import apps

from .forms import ItemForm, ToAddressForm, FromAddressForm, ContactForm, OptionsForm, BulkUploadForm
from .helpers import generate_quote_objects_in_db, bulk_import_quotes_at_options_select

from .models import Quote, QuoteItem, QuoteOptions, QuoteBol

from square.client import Client

import uuid
import logging

logger = logging.getLogger('other_file')
bulk_logger = logging.getLogger('bulk_import')
payment_errors_logger = logging.getLogger('payment_errors')
payment_logger = logging.getLogger('payments')


# Create your views here.
def create_quote(request):
    empty_item_formset = formset_factory(ItemForm, extra=1)
    empty_item_forms = empty_item_formset()
    empty_form = render_to_string('quotes/form/item-form.html', {'item_form': empty_item_forms[0]})
    empty_form = empty_form.replace('form-0', 'form-__prefix__')

    if request.method == 'POST':
        ItemFormSet = formset_factory(ItemForm)
        item_forms = ItemFormSet(request.POST)
        to_address = ToAddressForm(request.POST)
        from_address = FromAddressForm(request.POST)
        contact_form = ContactForm(request.POST)
        options_form = OptionsForm(request.POST)

        if item_forms.is_valid() and to_address.is_valid() and from_address.is_valid() and \
                contact_form.is_valid() and options_form.is_valid():

            item_forms_clean = item_forms.cleaned_data
            to_address_clean = to_address.cleaned_data
            from_address_clean = from_address.cleaned_data
            contact_form_clean = contact_form.cleaned_data
            options_form_clean = options_form.cleaned_data

            # get individual values
            from_info = {
                'name': from_address_clean['from_name'],
                'street': from_address_clean['from_street'],
                'city': from_address_clean['from_city'],
                'state': from_address_clean['from_state'],
                'zip': from_address_clean['from_zip'],
                'email': from_address_clean['from_email'],
                'phone': str(from_address_clean['from_phone']),
                'ref_number': from_address_clean['ref_number']
            }

            to_info = {
                'name': to_address_clean['to_name'],
                'street': to_address_clean['to_street'],
                'city': to_address_clean['to_city'],
                'state': to_address_clean['to_state'],
                'zip': to_address_clean['to_zip'],
                'phone': str(to_address_clean['to_phone']),
                'email': to_address_clean['to_email']
            }

            items = []
            for item_form in item_forms_clean:
                item = {
                    'quantity': item_form['quantity'],
                    'description': item_form['description'],
                    'weight': str(item_form['weight']),
                    'length': str(item_form['length']),
                    'width': str(item_form['width']),
                    'height': str(item_form['height']),
                    'value': str(item_form['value']),
                }
                items.append(item)

            bill_to_info = {
                'name': contact_form_clean['bill_to_name'],
                'phone': str(contact_form_clean['bill_to_phone']),
                'email': contact_form_clean['bill_to_email']
            }

            designer_info = {
                'name': contact_form_clean['designer_name'],
                'phone': str(contact_form_clean['designer_phone']),
                'email': contact_form_clean['designer_email']
            }

            options_info = {
                'delivery_type': options_form_clean['delivery_type'],
                'delivery_notes': options_form_clean['delivery_notes'],
            }

            quote_obj = generate_quote_objects_in_db(
                from_info, to_info, bill_to_info, items, designer_info, options_info
            )

            return redirect('quotes:created-quote')
        else:
            context = {
                'item_forms': item_forms,
                'to_address': to_address,
                'from_address': from_address,
                'contact_form': contact_form,
                'options_form': options_form,
                'empty_form': empty_form,
            }
            return render(request, 'quotes/create-quote.html', context)

    else:
        ItemFormSet = formset_factory(ItemForm, extra=1)
        item_forms = ItemFormSet()
        to_address = ToAddressForm()
        from_address = FromAddressForm()
        contact_form = ContactForm()
        options_form = OptionsForm()

        context = {
            'item_forms': item_forms,
            'to_address': to_address,
            'from_address': from_address,
            'contact_form': contact_form,
            'options_form': options_form,
            'empty_form': empty_form,
        }
        return render(request, 'quotes/create-quote.html', context)


def created_quote(request):
    return render(request, 'quotes/completed-quote-form.html')


def labels(request, encoding):
    quote = Quote.objects.get(encoding=encoding)
    bols = QuoteBol.objects.filter(quote=quote)

    return render(request, 'quotes/quote-labels.html', {'quote': quote, 'bols': bols})


def option_select(request, encoding):
    quote = Quote.objects.get(encoding=encoding)

    if quote.paid:
        return redirect('quotes:quote-workflow', quote.encoding)

    quote_options = QuoteOptions.objects.filter(quote__encoding=encoding)
    if request.method == 'POST':
        try:
            selected_option = request.POST['choice']

            # loop through the options if it's selected on the form the set to selected.
            # if they are changing their option then set other options to false
            for quote_option in quote_options:
                if int(quote_option.id) == int(selected_option):
                    logger.info(f'{quote.encoding} setting option {quote_option} to true')
                    quote_option.selected_option = True
                    quote_option.save()
                elif quote_option.selected_option:
                    logger.info(f'{quote.encoding} setting option {quote_option} to false')
                    quote_option.selected_option = False
                    quote_option.save()

            quote.status = 'needs_payment'
            quote.save()

            return redirect('quotes:quote-pay', encoding=quote.encoding)

        except (KeyError, QuoteOptions.DoesNotExist):
            context = {
                'quote': quote,
                'quote_options': quote_options,
                'error_message': "You didn't select a choice.",
            }
            return render(request, 'quotes/option-select.html', context)
    else:
        context = {
            'quote': quote,
            'quote_options': quote_options,
        }
        return render(request, 'quotes/option-select.html', context)


def quote_pay(request, encoding):
    quote = Quote.objects.get(encoding=encoding)

    payment_logger.info(f'{quote.encoding} | {request.META}')

    context = {
        'quote': quote,
        'square_js_url': settings.SQUARE_JS_URL
    }
    if quote.paid:
        payment_logger.info(f'{quote.encoding} | Already paid')
        return redirect('quotes:quote-workflow', quote.encoding)

    if request.method == 'POST':
        payment_logger.info(f'{quote.encoding} |  POST')
        idempotency_key = request.session.get('idempotency_shipping_key')
        if not idempotency_key:
            payment_logger.info(f'{quote.encoding} |  idempotency_key not found')
            payment_logger.info(f'{quote.encoding} |  generating new idempotency_key')
            idempotency_key = str(uuid.uuid4())
            request.session['idempotency_shipping_key'] = idempotency_key

        payment_logger.info(f'{quote.encoding} |  idempotency_key: {idempotency_key}')

        nonce = request.session.get('nonce')
        if not nonce:
            payment_errors_logger.info(f'{quote.encoding} PayQuote nonce not found')
            payment_logger.info(f'{quote.encoding} PayQuote nonce not found')
        else:
            payment_logger.info(f'{quote.encoding} PayQuote nonce: {nonce}')

        payment_amount = quote.get_square_charge()
        square_payment_body = {
            'source_id': str(nonce),
            'idempotency_key': f'{str(idempotency_key)}',
            'amount_money': {
                'amount': payment_amount,
                'currency': 'USD'
            },
            'reference_id': quote.encoding,
        }

        payment_logger.info(f'{quote.encoding} PayQuote submitting payment with this info {square_payment_body}')

        client = Client(
            access_token=settings.SQUARE_ACCESS_TOKEN,
            environment=settings.SQUARE_ENVIRONMENT,
        )

        payments_api = client.payments
        payment_result = payments_api.create_payment(square_payment_body)

        request.session['idempotency_shipping_key'] = False
        request.session['nonce'] = False

        payment_logger.info(f'{quote.encoding} PayQuote payment_result: {str(payment_result)}')

        if payment_result.is_success():
            quote.paid = True
            quote.paid_amount = payment_amount / 100
            quote.paid_date = datetime.utcnow()
            quote.status = 'paid'
            quote.save()
            payment_logger.info(f'{quote.encoding} | payment successful')
            return render(request, 'quotes/quote-payment-complete.html', {'quote': quote})
        else:
            payment_errors_logger.info(f'{quote.encoding} PayQuote payment failed {payment_result.errors}')
            payment_logger.info(f'{quote.encoding} PayQuote payment failed {payment_result.errors}')
            payment_errors_logger.info(f'{payment_result}')
            context.update({'payment_errors': payment_result.errors})

    request.session['idempotency_shipping_key'] = str(uuid.uuid4())
    request.session['nonce'] = False

    return render(request, 'quotes/quote-payment.html', context)


def quote_labels(request, encoding):
    quote_items = QuoteItem.objects.get(quote__encoding=encoding)

    context = {
        'items': quote_items,
    }
    return render(request, 'quotes/quote_labels.html', context)


def quote_workflow(request, encoding):
    quote = Quote.objects.get(encoding=encoding)
    context = {
        'quote': quote,
    }
    return render(request, 'quotes/workflow.html', context)


def items(request, encoding):
    quote = Quote.objects.get(encoding=encoding)

    items = quote.get_items_in_quote()
    context = {
        'items': items,
    }
    return render(request, 'quotes/items.html', context)


@login_required(login_url='/admin/login/')
def packaging_view(request):
    packaging_items = QuoteItem.objects.filter(quote__status='ready_to_package').order_by('quote__date_modified')

    context = {
        'quote_items': packaging_items,
    }
    return render(request, 'quotes/packaging-quotes.html', context)


@login_required(login_url='/admin/login/')
def bulk_upload(request, auction):
    auction_model = apps.get_model('preforma_quotes', 'Auction')
    auction_obj = auction_model.objects.get(slug=auction)
    auction_house = auction_obj.auction_house.id

    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        logger.info(request.FILES)
        if form.is_valid():
            quotes = bulk_import_quotes_at_options_select(request.FILES['file'], auction_house)
            context = {
                'quotes': quotes,
            }
            bulk_logger.info(f'bulk upload of {len(quotes)} quotes')
            return render(request, 'quotes/bulk-upload-done.html', context)
    else:
        form = BulkUploadForm()

    context = {
        'form': form,
    }
    return render(request, 'quotes/bulk-upload.html', context)


def bulk_upload_done(request, *args, **kwargs):
    try:
        quotes = kwargs['quotes']
    except KeyError:
        quotes = []

    return render(request, 'quotes/bulk-upload-done.html', context={'quotes': quotes})
