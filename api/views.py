from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from quotes.models import Quote
from django.conf import settings


import json
import logging

app_logger = logging.getLogger('app_api')
payment_logger = logging.getLogger('payments')


@require_POST
def payment_nonce(request):
    payment_logger.info('order_nonce Received nonce')
    nonce = json.loads(request.body)['nonce']
    request.session['nonce'] = nonce
    payment_logger.info(f'order_nonce set nonce to {nonce}')
    return HttpResponse('ok')


@require_GET
def quote_cost(request):
    body = json.loads(request.body)
    quote = Quote.objects.get(pk=body['quote_id'])

    data = {
        'quote_cost': quote.get_cost
    }

    return JsonResponse(data, safe=False)


@require_GET
def square_app_id(request):
    data = {
        'square_app_id': settings.SQUARE_APP_ID,
        'square_location_id': settings.SQUARE_LOCATION_ID,
    }
    return JsonResponse(data, safe=False)
