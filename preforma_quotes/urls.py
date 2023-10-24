from django.urls import path
from . import views


app_name = 'preforma_quotes'
urlpatterns = [
    path('<slug:partner_type>/<slug:auction_slug>/', views.select_items, name='select_items'),
    path('<slug:partner_type>/<slug:auction_slug>/quote/', views.quote, name='quote'),
    path('<slug:partner_type>/<slug:auction_slug>/clear/', views.clear, name='clear'),
    path('blah/', views.blah, name='blah')
]
