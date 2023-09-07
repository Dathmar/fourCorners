from django.urls import path
from . import views


app_name = 'preforma_quotes'
urlpatterns = [
    path('auction/<slug:auction_slug>/', views.quote, name='quote'),
]
