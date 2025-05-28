from .views import *
from django.urls import path

app_name = 'hijau'

urlpatterns = [
    #include urls from hijau app
    path('list_kunjungan/', list_kunjungan, name='list_kunjungan'),
    path('create_kunjungan/', create_kunjungan, name='create_kunjungan'),
    path('update_kunjungan/<uuid:id_kunjungan>/', update_kunjungan, name='update_kunjungan'),
    path('delete_kunjungan/<uuid:id_kunjungan>/', delete_kunjungan, name='delete_kunjungan'),
    path('list_kunjungan/<uuid:id_kunjungan>/', list_kunjungan, name='list_kunjungan_detail'),
    path('list_perawatan/', list_perawatan, name='list_perawatan'),
    path('list_rekam_medis/', list_rekam_medis, name='list_rekam_medis'),

]