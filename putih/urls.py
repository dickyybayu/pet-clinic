from django.urls import include, path
from . import views


app_name = 'putih'

urlpatterns = [
    #include urls from hijau app
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_selection, name='register_selection'),
    path('register/role/<str:role>/', views.register_role, name='register_role'),  
    path('register/klien_individu/', views.register_klien_individu, name='register_klien_individu'),
    path('register/klien_perusahaan/', views.register_klien_perusahaan, name='register_klien_perusahaan'),
    path('register/front_desk/', views.register_front_desk, name='register_front_desk'),
    path('register/dokter/', views.register_dokter, name='register_dokter'),
    path('register/perawat_register/', views.register_perawat, name='register_perawat'),
    path('profil/update_front_desk/', views.update_front_desk, name='update_front_desk'),

    path('profil/update_password/', views.update_password, name='update_password'),
    
    path('profil/', views.show_profile, name='show_profile'),
    # path('profil/update/', views.update_klien, name='update_klien'),
    path('logout/', views.logout, name='logout'),


    path('profil/update_klien/', views.update_klien_individu, name='update_klien_individu'),
    path('profil/update_klien_perusahaan/', views.update_klien_perusahaan, name='update_klien_perusahaan'),
    path('profil/update_dokter/', views.update_dokter, name='update_dokter'),
    path('profil/update_perawat/', views.update_perawat, name='update_perawat'),
    path('profil/update_password_placeholder/', views.update_password_placeholder, name='update_password_placeholder'),
    path('update_klien_individu/<str:id_klien>/', views.update_klien_individu, name='update_klien_individu'),
    path('update_klien_perusahaan/<str:id_klien>/', views.update_klien_perusahaan, name='update_klien_perusahaan'),




    
]
