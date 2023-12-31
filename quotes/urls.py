from django.urls import path
from . import views


app_name = 'quotes'
urlpatterns = [
    path('quote/create/', views.create_quote, name='create-quote'),
    path('quote/created/', views.created_quote, name='created-quote'),
    path('quote/option-select/<str:encoding>/', views.option_select, name='option-select'),
    path('quote/labels/<str:encoding>/', views.labels, name='labels'),
    path('quote/pay/<str:encoding>/', views.quote_pay, name='quote-pay'),
    path('quote/<str:encoding>/',  views.quote_workflow, name='quote-workflow'),
    path('quote/items/<str:encoding>/', views.items, name='items'),
    path('packaging/', views.packaging_view, name='packaging'),
    path('bulk-upload/<slug:auction>/', views.bulk_upload, name='bulk-upload-auction'),
    path('bulk-import/<slug:auction>/', views.bulk_upload, name='bulk-upload-auction'),
    path('bulk-upload-done/', views.bulk_upload_done, name='bulk-upload-done'),
]
