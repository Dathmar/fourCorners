from django.apps import apps

from .models import Quote, QuoteItem
from .quote_emails import send_internal_email


def generate_quote_objects_in_db(from_info, to_info, bill_to_info, items, designer_info, options_info):
    quote_object = Quote(
        to_name=to_info['name'],
        to_email=to_info['email'],
        to_phone=to_info['phone'],
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
        bill_to_email=bill_to_info['email'],
        bill_to_phone=bill_to_info['phone'],

        designer_name=designer_info['name'],
        designer_email=designer_info['email'],
        designer_phone=designer_info['phone'],

        delivery_type=options_info['delivery_type'],
        delivery_notes=options_info['delivery_notes'],

        status='send_created_notification',
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
        try:
            box_model = apps.get_model('preforma_quotes', 'Box')
            box = box_model.objects.filter(id=int(item['box']))
            if box:
                item_obj.box = box.first()
            else:
                item_obj.box = None
        except KeyError:
            item_obj.box = None

        item_obj.save()

        quote_item_obj = QuoteItem(
            quote=quote_object,
            item=item_obj,
        )
        quote_item_obj.save()

    send_internal_email(quote_object)
    return quote_object
