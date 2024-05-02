from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from python_http_client.exceptions import HTTPError

import json
import logging

logger = logging.getLogger('other_file')


def send_internal_email(quote):
    message = Mail(
        to_emails=[To('orders@4cl.com'), To('asher.danner@gmail.com')],
        from_email='orders@4cl.com'
    )
    message.template_id = 'd-bf9e3db380c3495da6ed0fa0d1001492'

    data = {
        'from_info': quote.get_from_info(),
        'to_info': quote.get_to_info(),
        'bill_to_info': quote.get_bill_to_info(),
        'items': quote.get_items_in_quote(),
        'designer_info': quote.get_designer_info(),
        'options_info': quote.get_options_info(),
        'status': quote.status,
        'encoding': quote.encoding,
        'email_logo': quote.get_logo_url(),
        'email_closing': quote.get_email_closing(),
    }

    send_email(message=message, data=data, logger_note='Create Internal')


def send_tracking_external_email(quote):
    message = Mail(
        to_emails=[To(quote.bill_to_email)],
        from_email='orders@4cl.com'
    )
    tracking_url = quote.shipper.tracking_url
    tracking_number = quote.tracking_number

    if tracking_url:
        tracking_url = tracking_url.replace('{tracking}', tracking_number)
        message.template_id = 'd-fe20070b24534305a938a402e1c7ebbf'  # with button template
    else:
        tracking_url = False
        message.template_id = 'd-3ba42244cf0f4db687727c79b660fe47'  # with button template

    if not tracking_number:
        return None

    data = {
        'email_logo': quote.get_logo_url(),
        'email_closing': quote.get_email_closing(),
        'shipper': quote.shipper.name,
        'tracking_url': tracking_url,
        'tracking_number': quote.tracking_number,
    }

    send_email(message=message, data=data, logger_note='Tracking External')


def send_create_external_email(quote):
    message = Mail(
        to_emails=[To(quote.bill_to_email)],
        from_email='orders@4cl.com'
    )
    data = {
        'email_logo': quote.get_logo_url(),
        'email_closing': quote.get_email_closing(),
    }

    message.template_id = 'd-6af4e6842d2544fe969ecadceadbade4'
    send_email(message=message, data=data, logger_note='Create External')


def send_quote_options_external_email(quote):
    message = Mail(
        to_emails=[To(quote.bill_to_email)],
        from_email='orders@4cl.com',
    )
    options_url = quote.get_quote_options_url()
    data = {
        'options_url': options_url,
        'email_logo': quote.get_logo_url(),
        'email_closing': quote.get_email_closing(),
    }

    message.template_id = 'd-69c6bf4ea1854f22a1a9a19568319feb'
    send_email(message=message, data=data, logger_note='Quote Options External')


def send_quote_paid_external_email(quote):
    message = Mail(
        to_emails=[To(quote.bill_to_email)],
        from_email='orders@4cl.com',
    )

    data = {
        'first_name': quote.to_name,
        'from_address': f'{quote.from_city}, {quote.from_zip}',
        'to_address': f'{quote.to_city}, {quote.to_zip}',
        'payment_amount': quote.paid_amount,
        'email_logo': quote.get_logo_url(),
        'email_closing': quote.get_email_closing(),
    }

    message.template_id = 'd-9a829673fd184955a9db578fed36135c'
    send_email(message=message, data=data, logger_note='Quote Paid External')


def send_quote_label_external_email(quote):
    message = Mail(
        # to_emails=[To(quote.from_email), To(quote.to_email)],
        to_emails=[To(quote.bill_to_email), To(quote.from_email)],
        from_email='orders@4cl.com'
    )

    data = {
        'label_url': quote.get_label_url(),
        'delivery_window': quote.delivery_window,
        'pickup_window': quote.pickup_window,
        'email_logo': quote.get_logo_url(),
        'email_closing': quote.get_email_closing(),
    }

    message.template_id = 'd-7a2892575231434882d99cd51fb10715'
    send_email(message=message, data=data, logger_note='Quote Label External')


def send_delivered_external_email(quote):
    message = Mail(
        to_emails=[To(quote.bill_to_email)],
        from_email='orders@4cl.com'
    )

    data = {
        'email_logo': quote.get_logo_url(),
        'email_closing': quote.get_email_closing(),
    }

    message.template_id = 'd-80cd15eb0c21466ba6a22a78161d3cb8'
    send_email(message=message, data=data, logger_note='Quote Delivered External')


def send_email(message, data=None,  logger_note=''):
    sg = SendGridAPIClient(settings.SEND_GRID_API_KEY)
    logger.info(f'Sending {logger_note} email')

    if data:
        message.dynamic_template_data = data
        logger.info(json.dumps(data))

    try:
        response = sg.send(message)
        logger.info(f'{logger_note} sent')
        logger.info(f'{response.body}')
        logger.info(f'{response.headers}')
        logger.info(f'{response.status_code}')
    except HTTPError as e:
        logger.info(f'{logger_note} HTTPError')
        logger.info(f'{e.to_dict}')
    except Exception as e:
        logger.info(f'{logger_note} other exception {e}')