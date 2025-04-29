from django.urls import path
from . import views

app_name = 'kuning'

urlpatterns = [
    path('jenis-hewan/', views.list_jenis_hewan, name='jenis_list'),
    path('jenis-hewan/create/', views.create_jenis_hewan, name='jenis_create'),
    path('jenis-hewan/update/<str:id_jenis>/', views.update_jenis_hewan, name='jenis_update'),
    path('jenis-hewan/delete/<str:id_jenis>/', views.delete_jenis_hewan, name='jenis_delete'),
    path('hewan-peliharaan/', views.list_hewan, name='hewan_list'),
    path('hewan-peliharaan/create/', views.create_hewan, name='hewan_create'),
    path('hewan-peliharaan/update/<str:id_hewan>/', views.update_hewan, name='hewan_update'),
    path('hewan-peliharaan/delete/<str:id_hewan>/', views.delete_hewan, name='hewan_delete'),
]
