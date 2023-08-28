from django.urls import path, include
from . import views


app_name = 'account'
urlpatterns = [
    path('<str:phone_number>/', views.index, name='index'),
]
