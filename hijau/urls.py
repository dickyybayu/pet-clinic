from .views import *
from django.urls import path

app_name = 'hijau'

urlpatterns = [
    #include urls from hijau app
    path('list_kunjungan/', list_kunjungan, name='list_kunjungan'),
    path('list_perawatan/', list_perawatan, name='list_perawatan'),
    path('create_kunjungan/', create_kunjungan, name='create_kunjungan'),
    path('delete_kunjungan/<str:id_kunjungan>/', delete_kunjungan, name='delete_kunjungan'),
    path('kunjungan/<uuid:id_kunjungan>/update/', update_kunjungan, name='update_kunjungan'),
    path('rekam-medis/<uuid:id_kunjungan>/', show_rekam_medis, name='show_rekam_medis'),
    path('rekam-medis/<uuid:id_kunjungan>/create/', create_rekam_medis, name='create_rekam_medis'),  
    path('api/hewan/<str:no_identitas_klien>/', api_hewan_by_klien, name='api_hewan_by_klien'),
    path("delete-treatment/<uuid:id_kunjungan>/<str:kode_perawatan>", delete_treatment, name="delete_treatment"),
    path("update-treatment/<uuid:id_kunjungan>/<str:kode_perawatan>", update_treatment, name="update_treatment"),
    path("create-treatment/", create_treatment, name="create_treatment"),
    
    
]