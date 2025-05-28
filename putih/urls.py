from django.urls import include, path
from . import views


app_name = 'putih'

urlpatterns = [
    #include urls from hijau app
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_selection, name='register_selection'),
    path('register/klien_register/', views.register_klien, name='register_klien'),
    path('register/front_desk_register/', views.register_front_desk, name='register_front_desk'),
    path('profil/update_fron_tdesk/', views.update_front_desk, name='update_front_desk'),

    path('profil/update_password/', views.update_password, name='update_password'),
    path('register/<str:role>/', views.register_role, name='register_role'),    
    
    path('profil/<str:role>/', views.show_profile, name='show_profile'),
    path('profil/dokter/', views.show_profile_dokter, name='show_profile_dokter'),
    path('profil/perawat/', views.show_profile_perawat, name='show_profile_perawat'),
    path('profil/frontdesk/', views.show_profile_frontdesk, name='show_profile_frontdesk'),
    path('profil/update/', views.update_klien, name='update_klien'),
    path('logout/', views.logout, name='logout'),


    path('profil/update_klien/', views.update_klien_individu, name='update_klien_individu'),
    path('profil/update_klien_perusahaan/', views.update_klien_perusahaan, name='update_klien_perusahaan'),
    path('profil/update_dokter/', views.update_dokter, name='update_dokter'),
    path('profil/update_perawat/', views.update_perawat, name='update_perawat'),
    path('profil/update_password_placeholder/', views.update_password_placeholder, name='update_password_placeholder'),




    
]
