from django.apps import apps
from decimal import Decimal
from openpyxl import load_workbook
import phonenumbers

from django.conf import settings

from preforma_quotes.models import AuctionHouse, Box
from .models import Quote, QuoteItem, QuoteOptions
from .quote_emails import send_internal_email

import logging

logger = logging.getLogger('bulk_import')


def generate_quote_objects_in_db(from_info, to_info, bill_to_info, items, designer_info, options_info, payment_options=None, create_status='send_created_notification', auction_house=None):
    to_email = 'test@4cl.com'
    to_phone = '+12105551212'

    bill_to_email = 'test@4cl.com'
    bill_to_phone = '+12105551212'

    if to_info['email']:
        to_email = to_info['email']

    if to_info['phone']:
        to_phone = to_info['phone']

    if bill_to_info['email']:
        bill_to_email = bill_to_info['email']

    if bill_to_info['phone']:
        bill_to_phone = bill_to_info['phone']

    logger.info('creating quote in the database')
    logger.info(f'from info: {from_info}')
    logger.info(f'to info: {to_info}')
    logger.info(f'bill to info: {bill_to_info}')
    logger.info(f'items: {items}')
    logger.info(f'designer info: {designer_info}')
    logger.info(f'options info: {options_info}')
    logger.info(f'payment options: {payment_options}')
    logger.info(f'create status: {create_status}')

    logger.info(f'to_email:  {to_email}')
    logger.info(f'to_phone:  {to_phone}')
    logger.info(f'bill_to_email:  {bill_to_email}')
    logger.info(f'bill_to_phone:  {bill_to_phone}')

    quote_object = Quote(
        to_name=to_info['name'],
        to_email=to_email,
        to_phone=to_phone,
        to_street=to_info['street'],
        to_city=to_info['city'],
        to_state=to_info['state'],
        to_zip=to_info['zip'],

        from_name=from_info['name'],
        from_phone=from_info['phone'],
        from_street=from_info['street'],
        from_city=from_info['city'],
        from_state=from_info['state'],
        from_zip=from_info['zip'],

        reference_number=from_info['ref_number'],

        bill_to_name=bill_to_info['name'],
        bill_to_email=bill_to_email,
        bill_to_phone=bill_to_phone,
    
        designer_name=designer_info['name'],
        designer_email=designer_info['email'],
        designer_phone=designer_info['phone'],

        delivery_type=options_info['delivery_type'],
        delivery_notes=options_info['delivery_notes'],

        seller=auction_house,

        status=create_status,
    )
    quote_object.save()

    for item in items:
        item_model = apps.get_model('items', 'Item')
        item_obj = item_model.objects.create(
            quantity=item['quantity'],
            description=item['description'],
            weight=item['weight'],
            length=item['length'],
            width=item['width'],
            height=item['height'],
            value=item['value'],
        )
        if item['box']:
            try:
                box_model = apps.get_model('preforma_quotes', 'Box')
                box = box_model.objects.filter(id=int(item['box']))
                if box:
                    item_obj.box = box.first()
                else:
                    item_obj.box = None
            except KeyError:
                item_obj.box = None
        else:
            item_obj.box = None

        item_obj.save()

        quote_item_obj = QuoteItem(
            quote=quote_object,
            item=item_obj,
        )
        quote_item_obj.save()

    if payment_options:
        for payment_option in payment_options:
            option = QuoteOptions.objects.create(
                quote=quote_object,
                option_description=payment_option['description'],
                option_price=Decimal(payment_option['price']),
            )
            option.save()

    if settings.SQUARE_ENVIRONMENT == 'sandbox':
        logger.info(f'Mock sending internal email for quote {quote_object.encoding}')
    else:
        send_internal_email(quote_object)
    return quote_object


def bulk_import_quotes_at_options_select(xl_file_path, auction_house):
    """
    Opens an Excel file that has customer and item shipping information.  Creates orders at the workflow of
    option_select and sends automated e-mails.  This groups together customer by phone number or email address.
    It groups an order by the first phone number and e-mail address seen for each but combines if either match.
    
    :param xl_file_path: the path to the Excel file needed for upload.
    :param auction_house: the id of the auction house that is importing the file.
    
    :type xl_file_path: str
    :type auction_house: int
    
    :return: None
    """

    # this function really needs to be refactored.

    wb = load_workbook(xl_file_path, read_only=True, data_only=True, keep_vba=False, keep_links=False)
    ws = wb.active

    auction_house = AuctionHouse.objects.get(id=auction_house)
    
    # ws has to be ordered as
    # first name, last name, address, city, state, zip, phone number, email,
    # item description, length, width, height, weight, quantity, option 1, option 1 price etc. up to 4 options
    quotes = []
    first_row = True

    logger.info('Starting bulk import')

    from_info = {
        'name': auction_house.name,
        'phone': auction_house.phone_number,
        'street': auction_house.address,
        'city': auction_house.city,
        'state': auction_house.state,
        'zip': auction_house.zip_code,
        'ref_number': '',
    }

    designer_info = {
        'name': None,
        'email': None,
        'phone': None,
    }
    options_info = {
        'delivery_type': 'NA',
        'delivery_notes': None,
    }

    for row in ws.rows:
        if first_row:
            logger.info('Skipping header row')
            first_row = False
            continue

        to_info, bill_to_info, item, options = get_quote_information_from_row(row)
        if to_info:
            logger.info(f'Processing quote with phone {to_info["phone"]} and email {to_info["email"]}')

            # see if a quote exists and if so append the item to an existing quote.  Otherwise, create a new quote
            appended = False
            logger.info(f'number of quotes at check loop {len(quotes)}')
            for quote in quotes:
                # quotes are unique by phone an e-mail
                if (quote['to_info']['phone'] == to_info['phone'] and quote['to_info']['phone'] is not None) or (quote['to_info']['email'] == to_info['email'] and quote['to_info']['email'] is not None):
                    logger.info(f'Appending {item["description"]} to quote with phone {quote["to_info"]["phone"]} and email {quote["to_info"]["email"]}')

                    # if a phone number was not associated to the quote add it
                    if quote['to_info']['phone'] == '' and to_info['phone']:
                        logger.info(f'Appending phone number {to_info["phone"]} to quote')
                        quote['to_info']['phone'] = to_info['phone']

                    # if an e-mail was not associated to a quote add it
                    if quote['to_info']['email'] == '' and to_info['email']:
                        logger.info(f'Appending email {to_info["email"]} to quote')
                        quote['to_info']['email'] = to_info['email']

                    # add the item to the quote
                    quote['items'].append(item)
                    appended = True

                    # if there were no shipping options then add them to the quote.
                    if not quote['options']:
                        quote['options'] = options

                    # break out of the loop because we found a matching quote
                    break

            # if the item wasn't appended to the list and there is a phone number or email
            # then create a new quote with the items
            if not appended:
                logger.info(f'No existing quote found with phone {to_info["phone"]} and email {to_info["email"]} creating new quote.')
                quotes.append({
                    'from_info': from_info,
                    'to_info': to_info,
                    'bill_to_info': bill_to_info,
                    'designer_info': designer_info,
                    'options_info': options_info,
                    'items': [item],
                    'options': options
                })

    # now generate a quote in the database for each quote we created.
    quote_list = []
    logger.info(f'number of quotes at import {len(quotes)}')
    for quote in quotes:
        quote_obj = generate_quote_objects_in_db(
            quote['from_info'], quote['to_info'], quote['bill_to_info'], quote['items'],
            quote['designer_info'], quote['options_info'], payment_options=quote['options'],
            create_status='send_options_notification', auction_house=auction_house
        )
        quote_list.append(quote_obj)

    return quote_list


def blank_excel_row(row):
    for cell in row:
        if cell.value:
            return False

    return True


def get_quote_information_from_row(row):
    if blank_excel_row(row):
        logger.info('Skipping blank row')
        return None, None, None, None

    try:
        phone = phonenumbers.parse(str(row[6].value), settings.PHONENUMBER_DEFAULT_REGION)
    except Exception as e:
        logger.error(f'Error parsing phone number for {row[8].value} exception {e}')
        phone = None

    to_info = {
        'name': f'{row[0].value} {row[1].value}',
        'email': row[7].value,
        'phone': phone,
        'street': row[2].value,
        'city': row[3].value,
        'state': row[4].value,
        'zip': row[5].value,
    }
    bill_to_info = {
        'name': f'{row[0].value} {row[1].value}',
        'email': row[7].value,
        'phone': phone,
    }

    try:
        length = Decimal(row[9].value)
    except Exception as e:
        logger.error(f'Error parsing length for {row[8].value} exception {e}')
        length = 0

    try:
        width = Decimal(row[10].value)
    except Exception as e:
        logger.error(f'Error parsing width for {row[8].value} exception {e}')
        width = 0

    try:
        height = Decimal(row[11].value)
    except Exception as e:
        logger.error(f'Error parsing height for {row[8].value} exception {e}')
        height = 0

    try:
        weight = Decimal(row[12].value)
    except Exception as e:
        logger.error(f'Error parsing weight for {row[8].value} exception {e}')
        weight = 0

    try:
        quantity = int(row[13].value)
    except Exception as e:
        logger.error(f'Error parsing quantity for {row[8].value} exception {e}')
        quantity = 1

    volume = length * width * height

    item = {
        'description': row[8].value,
        'length': length,
        'width': width,
        'height': height,
        'weight': weight,
        'quantity': quantity,
        'value': 0,
        'volume': volume,
        'box': None
    }
    item['box'] = get_packaging_for_item(item)

    options = []
    if row[14].value is not None:
        options.append({
            'description': row[14].value,
            'price': row[15].value,
        })
    if row[16].value is not None:
        options.append({
            'description': row[16].value,
            'price': row[17].value,
        })
    if row[18].value is not None:
        options.append({
            'description': row[18].value,
            'price': row[19].value,
        })
    if row[20].value is not None:
        options.append({
            'description': row[20].value,
            'price': row[21].value,
        })

    return to_info, bill_to_info, item, options


def get_packaging_for_item(item):
    if item['volume'] == 0:
        return None

    boxes = Box.objects.filter(max_volume__gte=item['volume']).order_by('max_volume')

    # loop through all the boxes to see if the item fits in it.
    for box in boxes:
        # we have to check each length, width, height combination to see if an item will fit in the box
        # I just do this manually, but we could have used permutations to do this.  I think this is faster because
        # the logic will stop once a box is found.
        if (item['length'] <= box.max_item_length and item['width'] <= box.max_item_width
                and item['height'] <= box.max_item_height):
            return box.id

        if (item['length'] <= box.max_item_width and item['width'] <= box.max_item_height
                and item['height'] <= box.max_item_length):
            return box.id

        if (item['length'] <= box.max_item_height and item['width'] <= box.max_item_length
                and item['height'] <= box.max_item_width):
            return box.id

    return None


def get_header_indexes(ws, header_row_num=0, normalize_header=False):
    """
    :param ws: the worksheet to process
    :param header_row_num: the row number of the header row
    :param normalize_header: whether to normalize the header names to lowercase and strip whitespace

    :type ws: openpyxl.worksheet.worksheet.Worksheet
    :type header_row_num: int
    :type normalize_header: bool

    :return: a dictionary of column names and their indexes
    """
    if normalize_header:
        return {str(cell.value).casefold().strip(): n for n, cell in enumerate(ws.rows[header_row_num])}
    else:
        return {cell.value: n for n, cell in enumerate(ws.rows[header_row_num])}

