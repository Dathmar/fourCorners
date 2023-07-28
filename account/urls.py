from django.urls import path, include
from . import views


app_name = 'api'
urlpatterns = [
    path('<str:phone_number>/', views.index, name='index'),
]
