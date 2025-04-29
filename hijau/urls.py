from .views import *
from django.urls import path

app_name = 'hijau'

urlpatterns = [
    #include urls from hijau app
    path('list_kunjungan', list_kunjungan, name='list_kunjungan'),
    path('list_treatment', list_treatment, name='list_treatment'),
    path('create_treatment', create_treatment, name='create_treatment'),
    path('update_treatment', update_treatment, name='update_treatment'),
    path('create_kunjungan', create_kunjungan, name='create_kunjungan'),
    path('create_rekam_medis', create_rekam_medis, name='create_rekam_medis'),
    path('show_rekam_medis', show_rekam_medis, name='show_rekam_medis'),
    path('update_rekam_medis', update_rekam_medis, name='update_rekam_medis'),
    path('update_kunjungan', update_kunjungan, name='update_kunjungan'),
    
]