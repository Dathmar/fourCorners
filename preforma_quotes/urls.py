from django.urls import path
from . import views


app_name = 'preforma_quotes'
urlpatterns = [
    path('auction/<slug:auction_slug>/', views.select_items, name='select_items'),
    path('auction/<slug:auction_slug>/quote/', views.quote, name='quote'),
    path('auction/<slug:auction_slug>/clear/', views.clear, name='clear'),
    path('blah/', views.blah, name='blah')
]
