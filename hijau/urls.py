from .views import *
from django.urls import path

app_name = 'hijau'

urlpatterns = [
    #include urls from hijau app
    path('list_hewan', list_hewan, name='list_hewan'),  
    path('list_kunjungan', list_kunjungan, name='list_kunjungan'),

    
]