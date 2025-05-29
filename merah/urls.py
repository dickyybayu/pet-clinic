from django.urls import path
from . import views

app_name = 'merah'

urlpatterns = [
    path('show_vaksinasi/', views.show_vaksinasi, name='show_vaksinasi'),  
    path('create_vaksinasi/', views.create_vaksinasi, name='create_vaksinasi'),
    path('update_vaksinasi/<str:id_kunjungan>/', views.update_vaksinasi, name='update_vaksinasi'),
    path('delete_vaksinasi/<str:id_kunjungan>/', views.delete_vaksinasi, name='delete_vaksinasi'),
    path('show_vaksin/', views.show_vaksin, name='show_vaksin'),
    path('create_vaksin/', views.create_vaksin, name='create_vaksin'),
    path('update_vaksin/<str:kode_vaksin>/', views.update_vaksin, name='update_vaksin'),
    path('update_stok_vaksin/<str:kode_vaksin>/', views.update_stok_vaksin, name='update_stok_vaksin'),
    path('delete_vaksin/<str:kode_vaksin>/', views.delete_vaksin, name='delete_vaksin'),
    path('show_data_klien/', views.show_data_klien, name='show_data_klien'),
    path('show_data_klien/<str:no_identitas>/', views.show_klien_detail, name='show_klien_detail'),
]
