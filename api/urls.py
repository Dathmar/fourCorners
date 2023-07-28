from django.urls import path, include
from . import views


app_name = 'api'
urlpatterns = [
    path('v1/quote-cost/', views.quote_cost, name='get-quote-cost'),
    path('v1/payment-nonce/', views.payment_nonce, name='payment-nonce'),
    path('v1/square-app-id/', views.square_app_id, name='square-app-id'),
]
