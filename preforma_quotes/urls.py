from django.urls import path
from . import views


app_name = 'preforma_quotes'
urlpatterns = [
    path('auction/new-orleans', views.quote, name='quote'),
]
