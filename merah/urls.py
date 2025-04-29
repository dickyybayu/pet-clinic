from django.urls import path
from . import views

app_name = 'merah'

urlpatterns = [
    path('show_vaksinasi/', views.show_vaksinasi, name='show_vaksinasi'),  
    path('create_vaksinasi/', views.create_vaksinasi, name='create_vaksinasi'),
    path('update_vaksinasi/<str:id_kunjungan>/cls', views.update_vaksinasi, name='update_vaksinasi'),
    path('delete_vaksinasi/<str:id_kunjungan>/', views.delete_vaksinasi, name='delete_vaksinasi'),
]
