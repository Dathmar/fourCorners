from django.http import JsonResponse, HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseServerError
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

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


@require_POST
@login_required
def move_quote_to_packaged(request, quote_id):
    quote = Quote.objects.get(pk=quote_id)

    if not quote:
        return Http404

    if not quote.ready_to_package():
        return HttpResponseNotAllowed

    if quote.move_to_packaged():
        return HttpResponse(status=200)
    else:
        return HttpResponseServerError
